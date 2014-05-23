#include <map>
#include <vector>
#include <iostream>
#include <algorithm>
#include <iterator>

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


int whos_turn(const vector<char>  & field){
	int x = std::count(field.begin(), field.end(), X_SYM);
	int o = std::count(field.begin(), field.end(), O_SYM);
	if (x < o){
		return X_MARK;
	}else{
		return O_MARK;
	}
}

pair<int, int> turn(const vector<char> & field, int turn){
	int potential[FLDSIZE*FLDSIZE];
	std::fill(potential, potential + FLDSIZE*FLDSIZE, 0);
	int best = -1; //initialize

	for (int i = 0 ; i < FLDSIZE; ++i){
		for (int j = 0; j < FLDSIZE; ++j){
			char c = field[i*FLDSIZE + j];
			int m = c==X_SYM?X_MARK:(c==O_SYM?O_MARK:0);
			if (m != 0){
				for (int l = 0; l < FLDSIZE; ++l)
					potential[l*FLDSIZE + j] += m;
				for (int l = 0; l < FLDSIZE; ++l)
					potential[i*FLDSIZE + l] += m;
				if (i == j){
					for (int l = 0; l < FLDSIZE; ++l)
						potential[l*FLDSIZE + l] += m;
				}
				if (i + j == FLDSIZE - 1){
					for (int l = 0; l < FLDSIZE; ++l)
						potential[l*FLDSIZE +FLDSIZE - 1 - l] += m;
				}
			}else{
				best = i*FLDSIZE + j;
			}
		}
	}

	for (int i = 0; i < FLDSIZE*FLDSIZE; i++)
		if (field[i] != X_SYM && field[i] != O_SYM)
		if ((turn == X_MARK && potential[best] < potential[i])||
			(turn == O_MARK && potential[best] > potential[i]))
			best = i;
	return std::make_pair(best/FLDSIZE, best%FLDSIZE);
}

int main(){
	//read inp field
	vector<char> field(9);

	for (int i = 0; i != 9; ++i){
	    cin >> field[0];
	}
	
    //analyse field
	int my_turn = whos_turn(field);
	pair<int, int> pos = turn(field, my_turn);
	//output move
	cout << pos.first << ' ' << pos.second<<endl;

	return 0;
}
