-- Migration 009: Partition translation_dictionary by POS group (pos_group),
-- rebuild indexes for the real query patterns, enable pg_trgm for fuzzy search.

-- 1. Trigram extension for typo-tolerant search (similarity(), % operator)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- 2. Lowercase source side of phrase dictionary so plain btree indexes apply
UPDATE phrase_dictionary
SET source_phrase = LOWER(source_phrase)
WHERE source_phrase <> LOWER(source_phrase);

-- 3. Convert translation_dictionary -> PARTITION BY LIST (pos_group)
DO $$
BEGIN
    -- already converted -> nothing to do
    IF to_regclass('translation_dictionary') IS NOT NULL
       AND EXISTS (
           SELECT 1 FROM pg_partitioned_table
           WHERE partrelid = 'translation_dictionary'::regclass
       ) THEN
        RETURN;
    END IF;

    IF to_regclass('translation_dictionary') IS NULL THEN
        RETURN;
    END IF;

    CREATE TABLE translation_dictionary_new (
        id BIGSERIAL,
        source_word TEXT NOT NULL,
        target_word TEXT NOT NULL,
        source_pos TEXT NOT NULL DEFAULT '',
        target_pos TEXT NOT NULL DEFAULT '',
        pos_group TEXT NOT NULL DEFAULT 'other',
        frequency INTEGER NOT NULL DEFAULT 1,
        PRIMARY KEY (id, pos_group)
    ) PARTITION BY LIST (pos_group);

    CREATE TABLE dict_part_noun  PARTITION OF translation_dictionary_new FOR VALUES IN ('noun');
    CREATE TABLE dict_part_verb  PARTITION OF translation_dictionary_new FOR VALUES IN ('verb');
    CREATE TABLE dict_part_adj   PARTITION OF translation_dictionary_new FOR VALUES IN ('adj');
    CREATE TABLE dict_part_adv   PARTITION OF translation_dictionary_new FOR VALUES IN ('adv');
    CREATE TABLE dict_part_func  PARTITION OF translation_dictionary_new FOR VALUES IN ('func');
    CREATE TABLE dict_part_other PARTITION OF translation_dictionary_new FOR VALUES IN ('other');

    -- Backfill: lowercase source, map fine POS tag -> coarse pos_group.
    -- DISTINCT ON guards against case-collisions created by lowering.
    INSERT INTO translation_dictionary_new
        (id, source_word, target_word, source_pos, target_pos, pos_group, frequency)
    SELECT DISTINCT ON (
               LOWER(source_word), target_word, source_pos,
               CASE
                   WHEN UPPER(source_pos) LIKE 'NN%' OR UPPER(source_pos) IN ('NC', 'N') THEN 'noun'
                   WHEN UPPER(source_pos) LIKE 'VB%' OR UPPER(source_pos) IN ('V', 'VERB') THEN 'verb'
                   WHEN UPPER(source_pos) LIKE 'JJ%' OR UPPER(source_pos) IN ('ADJ', 'A', 'S') THEN 'adj'
                   WHEN UPPER(source_pos) LIKE 'RB%' OR UPPER(source_pos) IN ('ADV', 'R') THEN 'adv'
                   WHEN UPPER(source_pos) IN (
                       'IN','TO','CC','DT','EX','WDT','WP','WP$','WRB','PRP','PRP$',
                       'MD','POS','RP','UH','PDT','FW','SYM','CD',
                       'DET','PRE','CON','PRO','NUM','INT','PONCT'
                   ) THEN 'func'
                   ELSE 'other'
               END
           )
           id,
           LOWER(source_word),
           target_word,
           source_pos,
           target_pos,
           CASE
               WHEN UPPER(source_pos) LIKE 'NN%' OR UPPER(source_pos) IN ('NC', 'N') THEN 'noun'
               WHEN UPPER(source_pos) LIKE 'VB%' OR UPPER(source_pos) IN ('V', 'VERB') THEN 'verb'
               WHEN UPPER(source_pos) LIKE 'JJ%' OR UPPER(source_pos) IN ('ADJ', 'A', 'S') THEN 'adj'
               WHEN UPPER(source_pos) LIKE 'RB%' OR UPPER(source_pos) IN ('ADV', 'R') THEN 'adv'
               WHEN UPPER(source_pos) IN (
                   'IN','TO','CC','DT','EX','WDT','WP','WP$','WRB','PRP','PRP$',
                   'MD','POS','RP','UH','PDT','FW','SYM','CD',
                   'DET','PRE','CON','PRO','NUM','INT','PONCT'
               ) THEN 'func'
               ELSE 'other'
           END,
           frequency
    FROM translation_dictionary
    ORDER BY LOWER(source_word), target_word, source_pos,
             CASE
                 WHEN UPPER(source_pos) LIKE 'NN%' OR UPPER(source_pos) IN ('NC', 'N') THEN 'noun'
                 WHEN UPPER(source_pos) LIKE 'VB%' OR UPPER(source_pos) IN ('V', 'VERB') THEN 'verb'
                 WHEN UPPER(source_pos) LIKE 'JJ%' OR UPPER(source_pos) IN ('ADJ', 'A', 'S') THEN 'adj'
                 WHEN UPPER(source_pos) LIKE 'RB%' OR UPPER(source_pos) IN ('ADV', 'R') THEN 'adv'
                 WHEN UPPER(source_pos) IN (
                     'IN','TO','CC','DT','EX','WDT','WP','WP$','WRB','PRP','PRP$',
                     'MD','POS','RP','UH','PDT','FW','SYM','CD',
                     'DET','PRE','CON','PRO','NUM','INT','PONCT'
                 ) THEN 'func'
                 ELSE 'other'
             END,
             frequency DESC, id;

    PERFORM setval(
        pg_get_serial_sequence('translation_dictionary_new', 'id'),
        GREATEST((SELECT COALESCE(MAX(id), 0) FROM translation_dictionary_new), 1)
    );

    DROP TABLE translation_dictionary;
    ALTER TABLE translation_dictionary_new RENAME TO translation_dictionary;

    -- Unique key MUST include the partition key (PG requirement for ON CONFLICT
    -- inference and for uniqueness on partitioned tables).
    CREATE UNIQUE INDEX idx_dict_unique
        ON translation_dictionary (source_word, target_word, source_pos, pos_group);

    -- Covering index for the hot lookup: source_word [+ pos_group pruning]
    -- returns target/pos/frequency straight from the index (index-only scan).
    CREATE INDEX idx_dict_source_pos
        ON translation_dictionary (source_word, source_pos)
        INCLUDE (target_word, target_pos, frequency);

    -- Prefix search (LIKE 'abc%') without LOWER() so the btree actually applies
    CREATE INDEX idx_dict_source_pattern
        ON translation_dictionary (source_word text_pattern_ops);

    -- Fuzzy/typo search: GIN trigram index powering similarity() and the % operator
    CREATE INDEX idx_dict_trgm
        ON translation_dictionary USING gin (source_word gin_trgm_ops);

    -- get_all() pagination: ORDER BY frequency DESC
    CREATE INDEX idx_dict_freq
        ON translation_dictionary (frequency DESC);
END $$;
