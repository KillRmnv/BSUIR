#include <iostream>
#include<set>
#include<math.h>

using int64 = long long;

int64 modexp(int64 base, int64 exp, int64 mod) {
    int64 result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) {
            result = (result * base) % mod; 
        }
        base = (base * base) % mod;
        exp >>= 1;
    }
    return result;
}
int primitive_element(int prime_num){
    for(int num=2;num<prime_num;num++){
        std::set<long unsigned int> field;
        for(int p=1;field.size()<=prime_num&&p<prime_num;p++){
            long unsigned int result=modexp(num, p, prime_num);
            if(field.find(result)==field.end()){
                field.insert(result);
            }else{
                field.clear();
                break;
            }
        }
        if(field.size()>0){
            return num;
        }
    }
    return 0;
}
int generate_secret(int primitive_el,int prime_num,int a,int  b){
    long unsigned int A=modexp(primitive_el, a, prime_num),
    B=modexp(primitive_el, b, prime_num);

    long unsigned int A1=modexp(B, a, prime_num),
    B1=modexp(A, b, prime_num);
    
    if(A1==B1){
        return A1;
    }
    return -1;

}
int main(){
    int prime_num;
    std::cout<<"Введите простое число:";
    std::cin>>prime_num;
    int primitive_el=primitive_element(prime_num);
    std::cout<<"Примитивный элемент:"<<primitive_el<<std::endl<<"Введите число для Алисы:";
    int a,b;
    std::cin>>a;
    std::cout<<"Введите число для Боба:";
    std::cin>>b;
    std::cout<<"Общий секрет:"<<generate_secret( primitive_el,  prime_num,  a,  b)<<std::endl;

}