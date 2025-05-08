package by.romanov.ppois.Entities;

import lombok.Data;

import java.util.HashMap;

@Data
public class LawRegistry {
    private HashMap<Integer, Law> CRIMINAL_LAWS;
    private HashMap<Integer, Law> ADMIN_LAWS;

    public LawRegistry() {
        CRIMINAL_LAWS = new HashMap<>();
        ADMIN_LAWS = new HashMap<>();

        // Заполняем уголовные законы (CRIMINAL_LAWS)
        CRIMINAL_LAWS.put(1, new Law(1, "Убийство (ст. 105 УК РФ)", "Лишение свободы от 6 до 15 лет"));
        CRIMINAL_LAWS.put(2, new Law(2, "Кража (ст. 158 УК РФ)", "Штраф до 500 тыс. руб. или лишение свободы до 5 лет"));
        CRIMINAL_LAWS.put(3, new Law(3, "Мошенничество (ст. 159 УК РФ)", "Лишение свободы до 10 лет"));
        CRIMINAL_LAWS.put(4, new Law(4, "Грабеж (ст. 161 УК РФ)", "Лишение свободы до 7 лет"));
        CRIMINAL_LAWS.put(5, new Law(5, "Разбой (ст. 162 УК РФ)", "Лишение свободы от 8 до 15 лет"));
        CRIMINAL_LAWS.put(6, new Law(6, "Вымогательство (ст. 163 УК РФ)", "Лишение свободы до 15 лет"));
        CRIMINAL_LAWS.put(7, new Law(7, "Незаконный оборот наркотиков (ст. 228 УК РФ)", "Лишение свободы от 4 до 15 лет"));
        CRIMINAL_LAWS.put(8, new Law(8, "Насильственные действия сексуального характера (ст. 132 УК РФ)", "Лишение свободы от 3 до 20 лет"));
        CRIMINAL_LAWS.put(9, new Law(9, "Хулиганство (ст. 213 УК РФ)", "Лишение свободы до 7 лет"));
        CRIMINAL_LAWS.put(10, new Law(10, "ДТП с тяжкими последствиями (ст. 264 УК РФ)", "Лишение свободы до 9 лет"));

        // Заполняем административные законы (ADMIN_LAWS)
        ADMIN_LAWS.put(1, new Law(1, "Нарушение ПДД (ст. 12.9 КоАП РФ)", "Штраф от 500 до 5000 руб. или лишение прав"));
        ADMIN_LAWS.put(2, new Law(2, "Мелкое хулиганство (ст. 20.1 КоАП РФ)", "Штраф до 2,5 тыс. руб. или арест до 15 суток"));
        ADMIN_LAWS.put(3, new Law(3, "Распитие алкоголя в общественных местах (ст. 20.20 КоАП РФ)", "Штраф от 500 до 1500 руб."));
        ADMIN_LAWS.put(4, new Law(4, "Неуплата штрафа ГИБДД (ст. 20.25 КоАП РФ)", "Двойной штраф или арест до 15 суток"));
        ADMIN_LAWS.put(5, new Law(5, "Нарушение тишины ночью (региональные КоАП)", "Штраф от 1 до 5 тыс. руб."));
        ADMIN_LAWS.put(6, new Law(6, "Незаконная торговля (ст. 14.1 КоАП РФ)", "Штраф до 50 тыс. руб."));
        ADMIN_LAWS.put(7, new Law(7, "Нарушение санитарных норм (ст. 6.3 КоАП РФ)", "Штраф до 1 млн руб. или приостановка деятельности"));
        ADMIN_LAWS.put(8, new Law(8, "Оскорбление (ст. 5.61 КоАП РФ)", "Штраф до 100 тыс. руб."));
        ADMIN_LAWS.put(9, new Law(9, "Нарушение миграционного учета (ст. 18.8 КоАП РФ)", "Штраф до 7 тыс. руб. с депортацией"));
        ADMIN_LAWS.put(10, new Law(10, "Незаконная парковка (ст. 12.19 КоАП РФ)", "Штраф от 1 до 5 тыс. руб."));
    }


    public String printCriminalLaws() {
        StringBuilder laws = new StringBuilder();
        for (var law : CRIMINAL_LAWS.values()) {
            laws.append("Закон ");
            laws.append(law.getId());
            laws.append(" \n");
            laws.append(law.getDescription());
            laws.append("\n");
            laws.append(law.getPunishment());
            laws.append("\n");
        }
        return laws.toString();
    }

    public String printAdminLaws() {
        StringBuilder laws = new StringBuilder();

        for (var law : ADMIN_LAWS.values()) {
            laws.append("Закон ");
            laws.append(law.getId());
            laws.append(" \n");
            laws.append(law.getDescription());
            laws.append("\n");
            laws.append(law.getPunishment());
            laws.append("\n");
        }
        return laws.toString();
    }
}