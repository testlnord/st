#include <cstdlib>
#include <vector>
#include <iostream>
#include <iterator>
#include <ctime>

using std::vector;
using std::pair;

using std::cout;
using std::cin;
using std::endl;

const int FLDSIZE = 3;
const int X_MARK = 1;
const int O_MARK = -1;
const char X_SYM = 'x';
const char O_SYM = 'o';



pair<int, int> turn(const vector<char> & field){
	vector<int> free;
	for (int i = 0; i != field.size(); ++i){
		if (field[i] != X_SYM && field[i] != O_SYM){
			free.push_back(i);
		}
	}
	srand(time(NULL));
	int pos = free[rand()%free.size()];

	return std::make_pair(pos/FLDSIZE, pos%FLDSIZE);
}

int main(){
	//read inp field
	vector<char> field(9);
	
	for (int i = 0; i != 9; ++i){
	    cin >> field[i];
	}
	
	pair<int, int> pos = turn(field);
	//output move
	cout << pos.first << ' ' << pos.second<<endl;

	return 0;
}
