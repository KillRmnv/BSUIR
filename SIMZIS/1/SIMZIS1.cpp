#include <cstdlib>
#include <ctime>
#include <string>
#include <cmath>
#include <iostream>
#include <locale>
#include <chrono>
#include <thread>
#include <map>
#include <iomanip>
using namespace std;
using namespace std::chrono;
using namespace std::this_thread; 
wstring const characters = L"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789";
double alphabet_size = 76;
enum Source{SERVER=1,LOCAL=2,IDEAL=1};



void visualize_distribution(const wstring &password, const wstring &alphabet) {
    map<wchar_t, double> freq;

    for (wchar_t c : alphabet) {
        freq[c] = 0;
    }

    for (wchar_t c : password) {
        if (freq.find(c) != freq.end()) {
            freq[c]++;
        }
    }

    wcout << L"\nЧастотное распределение символов (в %):\n";

    int total = password.size();
    if (total == 0) {
        wcout << L"Пароль пустой!" << endl;
        return;
    }

    for (auto &p : freq) {
        p.second = (p.second / total) * 100.0;
    }

    double max_freq = 0;
    for (auto &p : freq) {
        if (p.second > max_freq) max_freq = p.second;
    }
    if (max_freq == 0) max_freq = 1; // чтобы не делить на 0

    // Вывод гистограммы
    for (auto &p : freq) {
        wcout << p.first << L" (" << fixed << setprecision(2) << setw(5) 
              << p.second << L"%): ";

        int bar_len = (int)((50 * p.second) / max_freq);
        for (int i = 0; i < bar_len; i++) {
            wcout << L"█";
        }
        wcout << endl;
    }
}


wstring generate_password(int len) {
    int seed = time(NULL);
    srand(seed);
    wstring result;
    
    for(int i = 0; i < len; i++) {
        int random_index = rand() % characters.length();
        result += characters[random_index];
    }
    return result;
}
double benchmark(Source source){
    auto start = high_resolution_clock::now();
    int amount_of_sleep=0;
    for(auto s:characters){
        amount_of_sleep++;
    }
    auto end = high_resolution_clock::now();

    auto duration = duration_cast<microseconds>(end - start);
    if(source==SERVER)
        return  duration.count()+amount_of_sleep*20000;
    else if(source==LOCAL)
       return  duration.count()+amount_of_sleep*100;
    else
        return  duration.count();
}

int main() {
    setlocale(LC_ALL, "");
    wcout.imbue(locale(""));
    wcout << L"Введите длину пароля:\n";
    int len;
    cin >> len;
    wstring password = generate_password(len);
    wcout << L"Ваш пароль: " << password << endl;
    wcout<<L"Выберите источник:\n1.Сервер\n2.Локальная машина\n3.Идеальные условия\n";
    int choice;
    cin>>choice;
    Source source=static_cast<Source>(choice);
     long  double guess_per_second = benchmark(source);
    wcout<<L"Время перебора одной позиции:"<<guess_per_second/1000<<L" милисекунд\n";
    long double time_needed = (pow(alphabet_size, len)*guess_per_second) / (76*1000000*2);
    wcout << L"Теоретическое время подбора(1 поток): " << time_needed << L" секунд" << endl<<time_needed/60<<L" минут"<<endl<<time_needed/3600<<L" часов"<<endl
    << time_needed/3600*24<<L" дней"<<endl;
    wcout<<L"Теоретическое время подбора(1 поток на позицию): " <<  time_needed/password.length() << L" секунд" << endl<<(time_needed/60)/password.length()
    <<L" минут"<<endl<<(time_needed/3600)*password.length()<<L" часов"<<endl
    << (time_needed/(3600*24))/password.length()<<L" дней"<<endl;
    visualize_distribution(password,characters);
    return 0;
}