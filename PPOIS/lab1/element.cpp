#include"element.h"
#include "sets.h"
using namespace sets_ns;
std::string sets_ns::Element::elmnt()
{
	return this->element;
}
Set* sets_ns::Element::Sub()
{
	return this->Subset;
}
Element Element::fill(const std::string& Element) {
	if (Element[0] == '{') {
		if (Element[1] == '}') {
			this->element = "{}";
			return *this;
		}
		this->Subset = new Set;
		this->Subset->parsing(Element);
	}
	else
		this->element = Element;
	return *this;
}
bool Element::compare_string(const Element& a, const Element& b) {
	return a.element < b.element;
}
bool sets_ns::Element::operator==(const Element& anthr_element) const
{
	if (this->element == anthr_element.element && this->element != "")
		return true;
	else
		if (*this->Subset == anthr_element.Subset && this->element == anthr_element.element) {
			return true;
		}
		else
			if (this->element == anthr_element.element && this->Subset == nullptr && anthr_element.Subset == nullptr)
				return true;
	return false;
}
void sets_ns::Element::del_subset()
{
	this->Subset->~Set();
}