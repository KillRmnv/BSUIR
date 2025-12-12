package pbz.Romanov.entities.search;

import lombok.Getter;
import lombok.Setter;
import pbz.Romanov.entities.HistoryRecord;

@Getter
@Setter
public class HistoryRecordSearch extends HistoryRecord {

    @Override
    public void setId(Integer id) {
        // Для поиска разрешаем любые значения, включая -1
        this.id = id;
    }

    @Override
    public void setDate(String date) {
        this.date = (date != null) ? date.trim() : null;
    }

    @Override
    public void setNumOfPublication(Integer numOfPublication) {
        this.numOfPublication = numOfPublication;
    }

    @Override
    public void setState(Integer state) {
        this.state = state;
    }

    @Override
    public void setSub(Integer sub) {
        this.sub = sub;
    }
}
