---
title: 题解--Codeforces Round 680 [C. Division]
date: 2024-10-02 22:44:09
tags: [题解,codeforces,质因数分解]
categories: 算法
typora-root-url: ./cf
typora-copy-images-to: ./cf
---



[C. Division](https://codeforces.com/contest/1445/problem/C)





### C. Division

Oleg's favorite subjects are History and Math, and his favorite branch of mathematics is division.

To improve his division skills, Oleg came up with $t$ pairs of integers $p_i$ and $q_i$ and for each pair decided to find the **greatest** integer $x_i$, such that:

-   $p_i$ is divisible by $x_i$;
-   $x_i$ is not divisible by $q_i$.

Oleg is really good at division and managed to find all the answers quickly, how about you?

**Input**

The first line contains an integer $t$ ($1 \le t \le 50$) — the number of pairs.

Each of the following $t$ lines contains two integers $p_i$ and $q_i$ ($1 \le p_i \le 10^{18}$; $2 \le q_i \le 10^{9}$) — the $i$\-th pair of integers.

**Output**

Print $t$ integers: the $i$\-th integer is the largest $x_i$ such that $p_i$ is divisible by $x_i$, but $x_i$ is not divisible by $q_i$.

One can show that there is always at least one value of $x_i$ satisfying the divisibility conditions for the given constraints.

#### 样例

```
输入:
3
10 4
12 6
179 822
输出:
10
4
179

```


----------

### 算法1
##### 分解质因数  

![image-20241002225028721](image-20241002225028721.png)

 

#### 参考文献
 [参考](https://blog.csdn.net/JdiLfc/article/details/109479448?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-109479448-blog-109470145.235^v43^pc_blog_bottom_relevance_base3&spm=1001.2101.3001.4242.1&utm_relevant_index=3) 
#### C++ 代码
```cpp
#include<iostream>
#include<cstdio>
#include<algorithm>
#include<cmath>
#include<vector>
#define ll long long
using namespace std;

int t;

vector<int> div(ll x)//质因数分解
{
	vector<int> res;
	for(ll i=2;i*i<=x;i++)
	{
		if(x%i==0)
		{
			res.push_back(i);
			while(x%i==0)
				x/=i;
		}
	}
	if(x!=1) res.push_back(x);
	return res;
}

int main()
{
    scanf("%d",&t);
    while(t--)
    {
       ll p,q;
       scanf("%lld%lld",&p,&q);
       if(p%q!=0)
       {
       	printf("%d\n",p);
       	continue;
	   }
       vector<int >a = div(q);//获取q的所有质因数
       ll res=1;
       for(int i=0;i<a.size();i++)//遍历q的全部因数
       {
       	 ll k=p;
       	 while(k%q==0)//如果剩下的数能被q整除 说明还有a[i]这个因数
       	 {
       	 	k/=a[i];
		 }
		 res=max(res,k);
	   }
	   printf("%lld\n",res);
    }
    return 0;
}
```