#define _USE_MATH_DEFINES
#include <iostream>
#include <cmath>
#include <map>
#include <vector>
using namespace std;

class B {
public:
	virtual double generate()
	{
		return 0;
	}
};

class LCG : public B
{
private:
	int x_value = 1234;
	int a = 19577;
	int c = 32159;
	int m = 65537;
public:
	double generate() override
	{
		x_value = (a * x_value + c) % m;
		return x_value / double(m);
	}
	int get_m()
	{
		return m;
	}
};

class QCG : public B
{
private:
	long long x_value = 1234;
	int a = 101427;
	int c = 321;
	long long m = pow(2, 31);
	int d = 201433;
public:
	double generate() override
	{
		x_value = ((d * x_value)*(d*x_value) + a * x_value + c) % m;
		return x_value / double(m);
	}
};

class FibGen :public B
{
private:
	int n = 50;
	long long val = 1;
	long long m = pow(2, 32);

	long long fib(int n)
	{
		if (n <= 1)
			return n;
		return fib(n - 1) + fib(n - 2);
	}
public:
	double generate()
	{
		val = (fib(n) + fib(n - 1)) % m;
		n++;
		return val / double(m);
	}
};

class ICG :public B
{
private:
	int m = pow(2, 8);
	int val = 1;
	int a = 101425;
	int c = 322;

	int imod()
	{
		val = val % m;
		for (int i = 1; i < m; i++)
		{
			if ((val * i) % m == 1)
				return i;
		}
		return 1;
	}
public:
	double generate() override
	{
		val = (a * imod() + c) % m;
		return val / double(m);
	}
	int get_m()
	{
		return m;
	}
};

class UnionGen :public B
{
private:
	LCG x;
	ICG y;
	int val = 0;
public:
	double generate() override
	{
		val = int((x.generate() * x.get_m() - y.generate() * y.get_m())) % x.get_m();
		return double(val) / x.get_m();
	}
};

class Sigma :public B
{
private:
	double val = 0;
	UnionGen ug;
public:
	double generate() override
	{
		for (int i = 0; i < 12; i++)
		{
			val += ug.generate();
		}
		val -= 6;
		return val;
	}
};

class Polar :public B
{
private:
	double v1, v2, u1, u2, x1, x2, s=0;
	LCG lcg;
	ICG inv;
	double transform()
	{
		u1 = lcg.generate();
		u2 = inv.generate();
		v1 = 2 * u1 - 1;
		v2 = 2 * u2 - 1;
		s = v1 * v1 + v2 * v2;
		return s;
	}
public:
	double generate() override
	{
		do
			s = transform();
		while (s >= 1);
		x1 = v1 * sqrt(-2 * log(s) / s);
		x2 = v2 * sqrt(-2 * log(s) / s);
		return x1 * x1 + x2 * x2;
	}
};

class CorrelationGen :public B
{
private:
	double x, u, v = 0;
	FibGen fib;
	ICG icg;

	double find_x()
	{
		while (u == 0)
			u = fib.generate();
		v = icg.generate();
		x = sqrt(8 / M_E) * (v - 0.5) / u;
		return x;
	}
public:
	double generate() override
	{
		x = find_x();
		if (x * x <= pow(5 - 4 * M_E, 0.25) * u)
			return x;
		while (x * x >= (pow(4 * M_E, -1.35) / u + 1.4))
			x = find_x();
		while (x * x > -4 * log(u))
			x = find_x();
		return x;
	}
};

class LogGen :public B
{
private:
	ICG icg;
	double x = 0;
public:
	double generate() override
	{
		x = -log(icg.generate());
		return x;
	}
};

class ArensGen :public B
{
private:
	ICG icg;
	double u, x, v, y;
	int a = 10;
	void find_x_y()
	{
		u = icg.generate();
		v = icg.generate();
		y = tan(M_PI * u);
		x = sqrt(2 * a - 1) * y + a - 1;
	}
	void check_x()
	{
		do
			find_x_y();
		while (x <= 0);
	}
public:
	double generate() override
	{
		do
			check_x();
		while (v > (1 + y * y) * exp((a - 1) * log(x / (a - 1)) - sqrt(2 * a - 1) * y));
		return x;
	}
};

vector<double> historgam(B obj, int type)
{
	
}

double menu(int number)
{
	if (number>0 && number < 11)
	{
		LCG clg;
		QCG qcg;
		FibGen fg;
		ICG icg;
		UnionGen ug;
		Sigma s;
		Polar p;
		CorrelationGen cg;
		LogGen lg;
		ArensGen ag;
		map<int, B> generators = { {1, clg}, {2, qcg}, {3, fg}, {4, icg}, {5, ug}, {6, s}, {7, p}, {8, cg}, {9, lg}, {10, ag} };
		B obj = generators[number];
		return obj.generate();
	}
	else
	{
		cout << "Generators numbers are from 1 to 10" << endl;
	}
}

int main()
{

	return 0;
}