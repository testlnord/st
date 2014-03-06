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

int whos_turn(const vector<char>  & field){
	int x = std::count(field.begin(), field.end(), 'x');
	int o = std::count(field.begin(), field.end(), 'o');
	if (x < o){
		return 1;
	}else{
		return -1;
	}
}

pair<int, int> turn(const vector<char> & field, int turn){
	int potential[FLDSIZE*FLDSIZE];
	std::fill(potential, potential + FLDSIZE*FLDSIZE, 0);
	for (int i = 0 ; i < FLDSIZE; ++i){
		for (int j = 0; j < FLDSIZE; ++j){
			char c = field[i*FLDSIZE + j];
			int m = c=='x'?1:(c=='o'?-1:0);
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
						potential[l*FLDSIZE +FLDSIZE -1 - l] += m;
				}
			}
		}
	}
	int best = 0;
	for (int i = 0; i < FLDSIZE*FLDSIZE; i++)
		if (field[i] != 'x' && field[i] != 'o')
		if ((turn > 0 && potential[best] < potential[i])||
			(turn < 0 && potential[best] > potential[i]))
			best = i;
	return std::make_pair(best/FLDSIZE, best%FLDSIZE);
}

int main(){
	//read inp field
	vector<char> field((std::istream_iterator<char>(cin)), 
 					   (std::istream_iterator<char>()));
	
    //analyse field
	int my_turn = whos_turn(field);
	pair<int, int> pos = turn(field, my_turn);
	//output move
	cout << pos.first << ' ' << pos.second<<endl;

	return 0;
}
