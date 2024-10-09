#include "input.h"
#include <sstream>
#include <streambuf>
#include <gtest/gtest.h>
using namespace sets_ns;
std::string Output(Set some_set) {
    std::streambuf* oldBuffer = std::cout.rdbuf();
    std::ostringstream newBuffer;
    std::cout.rdbuf(newBuffer.rdbuf());
    std::cout << some_set;
    std::cout.rdbuf(oldBuffer);
    return newBuffer.str();
}
TEST(TestOutput, SetWithoutSubsets) {
    Set some_set; std::string input = "{fdhb,3,io po,rert,78,-45}"; some_set.parsing(input);
    EXPECT_EQ(some_set.amnt_of_elements(), 6);
    EXPECT_EQ(Output(some_set), "{-45,3,78,fdhb,io po,rert}");
}
TEST(TestOutput, SetWithSubsets) {
    Set some_set; std::string input = "{fdhb,{fk,io,po,{78,-45}},io po,rert,78,-45}"; some_set.parsing(input);
    EXPECT_EQ(some_set.amnt_of_elements(), 6);
    EXPECT_EQ(Output(some_set), "{{{-45,78},fk,io,po},-45,78,fdhb,io po,rert}");
}
TEST(TestOutput, EmptySet) {
    Set some_set; std::string input = "{}"; some_set.parsing(input);
    EXPECT_EQ(some_set.amnt_of_elements(), 0);
    EXPECT_EQ(Output(some_set), "{}");
}
TEST(TestOutput, SetWithEmptySubsets) {
    Set some_set; std::string input = "{{},{{},{}}}"; some_set.parsing(input);
    EXPECT_EQ(some_set.amnt_of_elements(), 2);
    EXPECT_EQ(Output(some_set), "{{{},{}},{}}");
}
TEST(TestSearchOperator, SetWithEmptySubsets) {
    Set some_set; std::string input = "{{},{{},{}}}"; some_set.parsing(input);
    input = "{}";
    EXPECT_EQ(some_set[input], 1);
    input = "{{},{}}";
    EXPECT_EQ(some_set[input], 0);
    input = "tyu";
    EXPECT_EQ(some_set[input], -1);
}
TEST(TestSearchOperator, SetWithoutSubsets) {
    Set some_set; std::string input = "{fdhb,3,io po,rert,78,-45}"; some_set.parsing(input);
    input = "-45";
    EXPECT_EQ(some_set[input], 0);
    input = "3";
    EXPECT_EQ(some_set[input], 1);
    input = "78";
    EXPECT_EQ(some_set[input], 2);
    input = "fdhb";
    EXPECT_EQ(some_set[input], 3);
    input = "io po";
    EXPECT_EQ(some_set[input], 4);
    input = "rert";
    EXPECT_EQ(some_set[input], 5);

}
TEST(TestSearchOperator, SetWithSubsets) {
    Set some_set; std::string input = "{fdhb,{fk,io,po,{78,-45}},io po,rert,78,-45}"; some_set.parsing(input);
    input = "-45";
    EXPECT_EQ(some_set[input], 1);
    input = "3";
    EXPECT_EQ(some_set[input], -1);
    input = "78";
    EXPECT_EQ(some_set[input], 2);
    input = "fdhb";
    EXPECT_EQ(some_set[input], 3);
    input = "io po";
    EXPECT_EQ(some_set[input], 4);
    input = "rert";
    EXPECT_EQ(some_set[input], 5);
    input = "{{-45,78},fk,io,po}";
    EXPECT_EQ(some_set[input], 0);
    input = "{-45,78}";
    EXPECT_EQ(some_set[input], -1);

}
TEST(TestAmntOfElements, SetWithoutSubsets) {
    Set some_set; std::string input = "{fdhb,3,io po,rert,78,-45}"; some_set.parsing(input);
    EXPECT_EQ(some_set.amnt_of_elements(), 6);
}
TEST(TestAmntOfElements, SetWithSubsets) {
    Set some_set; std::string input = "{fdhb,{fk,io,po,{78,-45}},io po,rert,78,-45}"; some_set.parsing(input);
    EXPECT_EQ(some_set.amnt_of_elements(), 6);
}
TEST(TestAmntOfElements, EmptySet) {
    Set some_set; std::string input = "{}"; some_set.parsing(input);
    EXPECT_EQ(some_set.amnt_of_elements(), 0);
}
TEST(TestAmntOfElements, SetWithEmptySubsets) {
    Set some_set; std::string input = "{{},{{},{}}}"; some_set.parsing(input);
    EXPECT_EQ(some_set.amnt_of_elements(), 2);
}
TEST(TestEmptiness, SetWithoutSubsets) {
    Set some_set; std::string input = "{fdhb,3,io po,rert,78,-45}"; some_set.parsing(input);
    EXPECT_EQ(some_set.check_on_emptiness(), false);
}
TEST(TestEmptiness, SetWithSubsets) {
    Set some_set; std::string input = "{fdhb,{fk,io,po,{78,-45}},io po,rert,78,-45}"; some_set.parsing(input);
    EXPECT_EQ(some_set.check_on_emptiness(), false);
}
TEST(TestEmptiness, EmptySet) {
    Set some_set; std::string input = "{}"; some_set.parsing(input);
    EXPECT_EQ(some_set.check_on_emptiness(), true);
}
TEST(TestEmptiness, SetWithEmptySubsets) {
    Set some_set; std::string input = "{{},{{},{}}}"; some_set.parsing(input);
    EXPECT_EQ(some_set.check_on_emptiness(), false);
}
TEST(TestMerge, SetWithEmptySubsets_EQ) {
    Set num_1; std::string input = "{{},{{},{}}}"; num_1.parsing(input);
    Set num_2; std::string anthr_input = "{{},rty vyt,1}"; num_2.parsing(anthr_input);
    Set* num_3 = new Set; num_3->parsing("{{{},{}},{},1,rty vyt}");
    Set result; result = num_1 += num_2;
    if (Output(result) == Output(*num_3))
        EXPECT_EQ(Output(*num_3), "{{{},{}},1,rty vyt,{}}");
}
TEST(TestIntersection, SetWithEmptySubsets_EQ) {
    Set num_1; std::string input = "{{},{{},{}}}"; num_1.parsing(input);
    Set num_2; std::string anthr_input = "{{{},{}}}"; num_2.parsing(anthr_input);
    Set result; result = num_1 *= num_2;
    Set* num_3 = new Set; num_3->parsing("{{{},{}}}");
    if (Output(result) == Output(*num_3))
        EXPECT_EQ(Output(*num_3), "{{{},{}}}");
}
TEST(TestDifference, SetWithEmptySubsets_EQ) {
    Set num_1; std::string input = "{{},{{},{}}}"; num_1.parsing(input);
    Set num_2; std::string anthr_input = "{{{},{}}}"; num_2.parsing(anthr_input);
    Set result; result = num_1 -= num_2;
    Set* num_3 = new Set; num_3->parsing("{{}}");
    if (Output(result) == Output(*num_3))
        EXPECT_EQ(Output(*num_3), "{{}}");
}
TEST(TestInputCheck, IncorrectInput) {
    std::string input = "{dcddc,{gjh}}}"; Set some_set;
    EXPECT_EQ(some_set.check_on_input(input), false);
}
TEST(TestPowerSet, SimpleSet) {
    Set some_set; some_set.parsing("{1,2,3}"); some_set.PowerSet();
    EXPECT_EQ(Output(some_set), "{{},{1},{2},{1,2},{3},{1,3},{2,3},{1,2,3}}");
}
TEST(CheckInput, FromString) {
    std::istringstream line("    {      fd      hb,   3,     io      po,   re    rt      ,    78,    -    45   }     "); Input_set test_input;
    auto oldCinBuffer = std::cin.rdbuf(line.rdbuf());
    EXPECT_EQ(test_input.string_input(), "{fd hb,3,io po,re rt,78,-45}");
}
TEST(CheckInput, FromChar) {
    std::istringstream line("    {      fd      hb,3   ,     io      po,   re    rt      ,    78,    -    45   }     "); Input_set test_input;
    auto oldCinBuffer = std::cin.rdbuf(line.rdbuf());
    EXPECT_EQ(test_input.char_input(), "{fd hb,3,io po,re rt,78,-45}");
}
TEST(CheckInput, Creatingset) {
    Input_set test_input; std::istringstream line("    {      fd      hb,3   ,     io      po,   re    rt      ,    78,    -    45   }     ");
    auto oldCinBuffer = std::cin.rdbuf(line.rdbuf());
    test_input.string_input();
    Set some_set; test_input.Create_set(some_set);
    EXPECT_EQ(Output(some_set), "{-45,3,78,fd hb,io po,re rt}");
}
TEST(CheckDelete, SomeSet) {
    Set some_set; some_set.parsing("{fdhb,3,io po,rert,78,-45}");
    Input_set test_input; std::istringstream line("3");
    auto oldCinBuffer = std::cin.rdbuf(line.rdbuf());
    some_set.del_element(test_input);
    EXPECT_EQ(Output(some_set), "{-45,78,fdhb,io po,rert}");
}
TEST(TestMerge, SetWithEmptySubsets) {
    Set num_1; std::string input = "{{},{{},{}}}"; num_1.parsing(input);
    Set num_2; std::string anthr_input = "{{},rty vyt,1}"; num_2.parsing(anthr_input);
    Set* num_3 = new Set; num_3->parsing("{{{},{}},{},1,rty vyt}");
    Set result; result = num_1 + num_2;
    if (Output(result) == Output(*num_3))
        EXPECT_EQ(Output(*num_3), "{{{},{}},1,rty vyt,{}}");
}
TEST(TestIntersection, SetWithEmptySubsets) {
    Set num_1; std::string input = "{{},{{},{}}}"; num_1.parsing(input);
    Set num_2; std::string anthr_input = "{{{},{}}}"; num_2.parsing(anthr_input);
    Set result; result = num_1 * num_2;
    Set* num_3 = new Set; num_3->parsing("{{{},{}}}");
    if (Output(result) == Output(*num_3))
        EXPECT_EQ(Output(*num_3), "{{{},{}}}");
}
TEST(TestDifference, SetWithEmptySubsets) {
    Set num_1; std::string input = "{{},{{},{}}}"; num_1.parsing(input);
    Set num_2; std::string anthr_input = "{{{},{}}}"; num_2.parsing(anthr_input);
    Set result; result = num_1 - num_2;
    Set* num_3 = new Set; num_3->parsing("{{}}");
    if (Output(result) == Output(*num_3))
        EXPECT_EQ(Output(*num_3), "{{}}");
}
int main(int argc, char** argv) {
    setlocale(LC_ALL, "ru");
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS(); 
}