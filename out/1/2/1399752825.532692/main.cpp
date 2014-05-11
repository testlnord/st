#include <iostream>
#include "enumer.cpp"
using namespace std;



int plus2(int a){
	return a+2;
}
bool less4(int a){
	if (a <= 4){
		return true;
	}else{
		return false;
	}
}
int main(){
	vector<int> a(5,1);
	a[3] = 2;
	Enumerable e(a);
	Enumerable c =e.Select(plus2).Where(less4); 
	while (c.getEnumerator()->next()){
		cout << c.getEnumerator()->current() << endl;
	}
    //vector<int> b(c.toVector());
	//for (vector<int>::iterator it = b.begin(); it!= b.end(); ++it){
	//	cout << *it<< ' ';
	//}
	cout << endl;
	return 0;
}
