#define _USE_MATH_DEFINES
#include <iostream>
#include <cmath>
#include <map>
#include <vector>
#include <string>
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
		x_value = ((d * x_value) * (d * x_value) + a * x_value + c) % m;
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
		int n1 = 1;
		int n2 = 1;
		for (int i = 0; i < n - 2; i++)
		{
			int tmp = n1;
			n1 = n2;
			n2 += tmp;
		}
		return n2;
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
	double v1, v2, u1, u2, x1, x2, s = 0;
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
	double x=0, u=0, v = 0;
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
		if (x * x <= 5 - 4 * pow(M_E, 0.25) * u)
			return x;
		while (x * x >= (4 * pow(M_E, -1.35)) / u + 1.4)
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
	double u=0, x=0, v=0, y=0;
	const int a = 10;
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

vector<double> histogram(B& obj, int type)
{
	vector<double> res(10);
	if (type > 5 && type < 9)
		res.resize(7);
	for (int j = 0; j < 1000; j++)
	{
		double num = obj.generate();
		if (type < 6)
		{
			for (int i=0; i < 10; i++)
			{
				if (i / 10. <= num && num <= i / 10. + 0.1)
				{
					res[i] += 1;
					break;
				}
			}
		}
		else if (type < 9)
		{
			for (int i = -3; i < 4; i++)
			{
				if (i <= num && num <= i + 1)
				{
					res[i + 3] += 1;
					break;
				}
			}
		}
		else
		{
			for (int i = 0; i < 100; i+=10)
			{
				if (i <= num && num <= i + 1)
				{
					res[int(i/10)] += 1;
					break;
				}
			}
		}
	}
	for (int i = 0; i < res.size(); i++)
	{
		res[i] = res[i] / 1000;
	}
	return res;
}

double menu(int number)
{
	switch (number)
	{
	case 1:
	{
		LCG clg;
		return clg.generate();
	}
	case 2:
	{
		QCG qcg;
		return qcg.generate();
	}
	case 3:
	{
		FibGen fg;
		return fg.generate();
	}
	case 4:
	{
		ICG icg;
		return icg.generate();
	}
	case 5:
	{
		UnionGen ug;
		return ug.generate();
	}
	case 6:
	{
		Sigma s;
		return s.generate();
	}
	case 7:
	{
		Polar p;
		return p.generate();
	}
	case 8:
	{
		CorrelationGen cg;
		return cg.generate();
	}
	case 9:
	{
		LogGen lg;
		return lg.generate();
	}
	case 10:
	{
		ArensGen ag;
		return ag.generate();
	}
	default:
		return -1;
	}
}

int main()
{
	LCG lcg;
	double sum = 0;
	auto res1 = histogram(lcg, 1);
	cout << "1st generator" << endl;
	for (int i = 0; i < res1.size(); i++)
	{
		cout << res1[i] << endl;
		sum += res1[i];
	}
	cout << sum;
	return 0;
}