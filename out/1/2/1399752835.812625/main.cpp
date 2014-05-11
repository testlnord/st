#include <iostream>
#include <cmath>
#include <omp.h>
using namespace std;

double func(double x){
	return exp(x);
}

int main(){
	double inegr = 0;
	double step = 0.00001;
	double x = 0;
	double b = 1;
	int steps = (b-x)/step;
	int t_s = omp_get_max_threads();
	double* ress = new double[t_s];
	for (int i = 0; i < t_s; i++){
		ress[i] = 0;
	}
    #pragma omp parallel for shared(ress)
	for (int i = 0; i < steps; ++i ){
		//cout << omp_get_thread_num() << endl; 
		int k = omp_get_thread_num();
		ress[k] +=  (func((i+1)*step) + func(i*step))/2*step;

	}

	for (int i = 0; i < t_s; i++){
		inegr += ress[i];
		cout << ress[i] << " ";
	}
	cout << omp_get_max_threads() << endl;
	cout << inegr << endl;
	cout << 1.71828 << " wolfram" << endl;
}
