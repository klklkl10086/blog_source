---
title: Database
date: 2024-05-07 19:03:11
tags: SQL
categories: class
description: 数据库系统原理的部分笔记
typora-root-url: ./Database
---



**肯定有错，PPT来源于学校，如果侵权请通过邮箱告知**





# SQL初步

**Structed Query Language 结构化查询语言**

![Screenshot_20240507_190655_com.huawei.hinote](Screenshot_20240507_190655_com.huawei.hinote.png)



## 属性域的类型

> - char(n) 	固定长度字符串，用户指定长度为n，若输入为短于n的字符串，自动补空格
> - varchar(n)   可变长度字符串，最大长度为n，由用户指定
> - int      整数型
> - smallint     小整数
> - numeric(p,d)     定点小数，长度一共为p其中有d位小数，p与d由用户指定
> - real,double precision    浮点数 双精度浮点数
> - float(n)  精度为n的浮点数

## 完整性约束

```mysql
#非空约束：
not null
#主键约束  非空且唯一
primary key(A1,A2,...,An)
#外码约束
foreign key(A1,A3,...An) references r
```



## 创建表

```mysql
CREATE TABLE r(A1 D1,A2 D2,....,An Dn,
              (完整性约束1)，
              (完整性约束2)，
               .....，
               (完整性约束n)，
              )
```

**r是关系名字，A是属性名字，D是属性域类型**

![Screenshot_20240507_202654_com.huawei.hinote](Screenshot_20240507_202654_com.huawei.hinote.png)

![image-20240507203933365](image-20240507203933365.png)

```mysql
create table department(
    dept_name varchar(20),
    building varchar(15),
    budget numeric(12,2),
    primary key(dept_name)
);
create table instructor(
    ID char(5),
    _name varchar(20) not null,
    dept_name varchar(20),
    salary numeric(8,2),
    primary key(ID),
    foreign key(dept_name) references department(dept_name)
);
```



## Insert

```mysql
insert into R values ('','','',...,'');

insert into department values('Biology','biology','15000');
```

## Delete

```mysql
#保留关系，移除所有元组
delete from R

delete from student
```

## Drop

```mysql
#删除关系r
drop table r
```

## Alter

增删属性

```mysql
 alter table r add A D 
 alter table students add parent varchar(10);
 
 alter table r drop A
 alter table students drop parent;
```

**也可以用于创建表之后对表进行新的主码约束和非空限制等操作**



## 查询

![Screenshot_20240507_205222_com.huawei.hinote](Screenshot_20240507_205222_com.huawei.hinote.png)

**返回结果为关系**

**Select**

关系代数中的投影运算

```mysql
#选取所有列
select * 
from instructor;

select '2011';

select '2011' as year;

select 'A' 
from instructor;
```

![image-20240507205828047](image-20240507205828047.png)

![image-20240507205844996](image-20240507205844996.png)

![image-20240507205758202](image-20240507205758202.png)

```mysql
 select ID,name,salary/12 
 from instructor;
 
  select ID,name,salary/12 as monthly_salary
  from instructor;
```

**tips：**

1. **在sql中是不区分大小写的**
2. **sql中查询默认不会自动去重，想要去重需要加上distinct关键字，想要显示地不去重，可以使用all关键字**

```mysql
select distinct dept_name from instructor
```

```mysql
select all dept_name from instructor
```

​	3.**select  语句中可以包含算术表达式，比如= ,-,*,/作用于属性上**

```mysql
select ID, name, salary/12 from instructor

select ID, name, salary/12 as monthly_salary from instructor
```



**where**

- **限制选取元组的条件**，类似于关系代数的选择操作
- **可以使用 and or not 进行多个条件的连接，只有让where语句为true的元组才能被选中**

```mysql
select name
from instructor
where dept_name='Biology';

select name
from instructor
where dept_name='Biology' and salary>80;# and ,or, not
```

- **between 比较运算符表  [   ]（数学上的左闭右闭）**

```mysql
select name from instructor where salary between 90000 and 100000
```

- **元组比较**

```mysql
select name, course_id
from instructor, teaches
where (instructor.ID, dept_name) = (teaches.ID, 'Biology');
```



**from**

- **若from后面有多个关系，则是对多个关系进行笛卡尔乘积**，在进行where的判断，最后执行select
- **支持重命名操作**



## 更名

```mysql
oldname as newname
select ID,name,salary/12 as monthly_salary
  from instructor;
```

## 字符串

**like关键字**

> % :匹配任意字符串
>
> _ : 匹配任意字符

```mysql
select name 
from instructor 
where name like '%dar%' #选择含有dar的字符串

```

**escape关键字**

表转义字符

```mysql
like '100 \%'  escape  '\' 
#匹配“100%”字符串
```

**运算**

- 连接运算    ||  表连接
- 字符串匹配对大小写敏感

- 大小写转换
- 计算字符串长度等

## 排序 

**order by**

排列元组的**显示**顺序

**默认为升序，加上desc关键字表降序，也可以加asc显式地指出为升序**

```mysql
select distinct name
from instructor
order by name#根据name进行升序排序

select distinct name
from instructor
order by name desc#根据name进行降序排序

order by dept_name, name#多个属性为排序依据
order by dept_name desc, name asc

```

![image-20240508222044255](image-20240508222044255.png)

## 集合运算



**并  union**

```mysql
(select course_id from section where sem = ‘Fall' and year = 2009)
union
(select course_id from section where sem = ‘Spring' and year = 2010)
```

**交 intersect**

```mysql
(select course_id from section where sem = ‘Fall' and year = 2009)
intersect
(select course_id from section where sem = ‘Spring' and year = 2010)
```

**差 except**

```mysql
(select course_id from section where sem = ‘Fall' and year = 2009)
except
(select course_id from section where sem = ‘Spring' and year = 2010)
```

**sql上的集合运算自动去重**

**若想要保留重复元组，则要显式地指出，union all, intersect all  except all**



## Null 空值

- **表未知 unkonwn**

- **空值参与任何算术表达式的结果都是空值**

- **is null 可以用来检验是否是空值，如果是空值则返回true**

  ```mysql
  select name
  from instructor
  where salary is null
  ```

- **空值与逻辑运算**

  ![image-20240508223215396](image-20240508223215396.png)

- **如果where子句的谓词计算出的结果为false或者是unkonwn则元组不可出现在结果中**

## 聚集函数

> -   **avg:** average value
> -   **min:** minimum value
> -   **max:** maximum value
> -   **sum:** sum of values
> -   **count:** number of values
>
> **输入元组集合返回单个值**

- **avg，min，max，sum的作用对象必须是数字集**

- **除了count其他函数面对空值都视而不见，如果表中只有空值，count会返回0，其他函数范围null**

- **聚集函数只可以出现在select子句和having子句中，不可以出现在where中**

```mysql
select avg (salary)
from instructor
where dept_name= 'Comp. Sci.';

select count (distinct ID)
from teaches
where semester = 'Spring' and year = 2010;
```



## 分组

**group by**

```mysql
#分组聚合
select dept_name, avg (salary) as avg_salary
from instructor
group by dept_name;
```

**没有出现在select聚集函数中的属性必须出现在group by中，出现在group by中的属性不一定出现在select中**

## having

- **无group by无having，形成分组之后再应用having语句**
- **from -> where -> group by -> having -> select ->order by**

- **任何出现在having语句中但未被聚集的属性必须出现在group by语句中**

```mysql
select dept_name, avg (salary)
from instructor
group by dept_name
having avg (salary) > 42000;
```

## 嵌套子查询

**where**

- **集合成员资格**

  **in**：若在则true

  ```mysql
  select count (distinct ID)
  from takes
  where (course_id, sec_id, semester, year) in   
  							(select course_id, sec_id, semester, year
                                   from teaches
                                   where teaches.ID= 10101);
  ```

  **not in**：不在则true

  ```mysql
  select distinct course_id
  from section
  where semester = 'Fall' and year= 2009 and
  					course_id  not in (select course_id
                                          from section
                                          where semester = 'Spring'and year= 2010);
  
  ```

  

- **集合比较**

  **some**：至少有一个

  ```mysql
  select name
  from instructor
  where salary > some (select salary
                        from instructor
                        where dept name = 'Biology');
  #查询工资比同部门至少一个人高的生物系教授的名字
  ```

  ![image-20240510195352004](image-20240510195352004.png)

  

  

  **all**：全都

  ```mysql
  select name
  from instructor
  where salary > all (select salary
                     from instructor
                     where dept name = 'Biology');
   #查找生物系教授中工资最大（比同系其他教授都高）的教授名字
  ```

  ![image-20240510195712732](image-20240510195712732.png)

- **集合约束**



​		**空关系验证 exists** 

​		![image-20240510200104835](image-20240510200104835.png)

```mysql
select course_id
from section as S	#S被称作为相关名称
where semester = 'Fall' and year = 2009 and 
				exists (select * #内查询叫作相关子查询
                		from section as T
                        where semester = 'Spring'  
                        and year= 2010  and S.course_id = T.course_id);

```

```mysql
# Find all students who have taken all courses offered in the Biology department.
select distinct S.ID, S.name
from student as S
where not exists ( (select course_id  from course
                                 where dept_name = 'Biology')
                               except
                                 (select T.course_id  from takes as T
                                   where S.ID = T.ID));
```



​	**检查是否存在重复元组 unique** 

​	unique：**存在重复返回false，不存在则返回true**

​	not unique：**反之**

```mysql
#Find all courses that were offered at most once in 2009
select T.course_id
from course as T
where unique (select R.course_id  from section as R
				where T.course_id= R.course_id  and R.year = 2009);
```

**from**

```mysql
select dept_name, avg_salary
from (select dept_name, avg (salary) as avg_salary
      from instructor
      group by dept_name)
      where avg_salary > 42000;
或者
select dept_name, avg_salary
from (select dept_name, avg (salary) 
      from instructor
      group by dept_name) as dept_avg (dept_name, avg_salary)
    where avg_salary > 42000;

```

​	**with**

>**定义临时关系，只能在同一查询的后面使用**

```mysql
with max_budget (value) as  #max_budget 是临时关系
    (select max(budget)
     from department)
select department.name
from department, max_budget
where department.budget = max_budget.value;
```

```mysql
# Find all departments where the total salary is greater than the average of the total salary at all departments
with dept _total (dept_name, value) as
        (select dept_name, sum(salary)
         from instructor
         group by dept_name),
        dept_total_avg(value) as
        ( select avg(value)
          from dept_total )
select dept_name
from dept_total, dept_total_avg
where dept_total.value > dept_total_avg.value;
```

**select**

> **标量子查询：用在 只返回一个包含单个属性的元组的查询 的地方**
>
> **如果子查询返回多于一个结果的元组会出现error**

```mysql
select dept_name, ( select count(*)  from instructor                                 					where department.dept_name = instructor.dept_name)                               as num_instructors
from department;
```



## 删除

**delete**

>- **delet只能删除元组**
>- **一个delete只能作用与一个关系上**

```mysql
#Delete all instructors
delete from instructor 

#Delete all instructors from the Finance department
delete from instructor where dept_name= 'Finance';

#Delete all tuples in the instructor relation for those instructors associated with a department located in the Watson building.
delete from instructor
where dept_name in ( select dept name
                    from department
                    where building = 'Watson');
```



```mysql
#a funny example:
delete from instructor
where salary < (select avg (salary) 
                           from instructor);
#Problem:  as we delete tuples from deposit, the average salary changes,边删除平均值边改变
#Solution used in SQL:
#1.   First, compute avg (salary) and find all tuples to delete
#2.   Next, delete all tuples found above (without recomputing  avg or retesting the tuples) 
```

## 插入

**insert**



```mysql
insert into course
values ('CS-437', 'Database Systems', 'Comp. Sci.', 4);
#or equivalently
insert into course (course_id, title, dept_name, credits)
values ('CS-437', 'Database Systems', 'Comp. Sci.', 4);
```

```mysql
#Add a new tuple to student with tot_creds set to null
insert into student
values ('3003', 'Green', 'Finance', null);
```

> **系统在执行任何插入之前先执行完select语句十分重要**
>
> **Otherwise** queries like
>
> ​     **insert into** *table*1 **select** * **from** *table*1
>
>  would cause problem



## 更新

**update**

> 改变某个元组的某个属性的值
>
> update table1
>
> ​	set  attribute1 [ ]
>
> ​	where 

```mysql
#Increase salaries of instructors whose salary is over $100,000 by 3%, and all others by a 5% 
update instructor
	set salary = salary * 1.03
	where salary > 100000;
update instructor
	set salary = salary * 1.05
	where salary <= 100000;
#顺序很重要，不能两次更新不能交换位置
```

**case**

>case
>
>​	when  predict1  then  result1
>
>​	when predict2  then  result2
>
>​	......
>
>​	else result
>
>end

```mysql
#可以用case语句进行书写
update instructor
set salary = case
	when salary <= 100000 then salary * 1.05
						else salary * 1.03
end
```

**update 与标量子查询**

```mysql
#Recompute and update tot_creds value for all students
update student S 
set tot_cred = ( select sum(credits)
                from takes, course
                where takes.course_id = course.course_id and 
                S.ID= takes.ID.and  takes.grade <> 'F' and 
                                              takes.grade is not null );
#Instead of sum(credits), use:
case
when sum(credits) is not null then sum(credits)
else 0
end
```

# SQL进阶

## 连接

> join ：输入两个关系返回一个关系
>
> ![image-20240513103308652](image-20240513103308652.png)

![image-20240513103317354](image-20240513103317354.png)

### 自然连接

> ```
> 自然连接基于相同的属性名称和数据类型连接两个表。结果表将包含两个表的所有属性，但每个公共列仅保留一份副本
> ```

### 内连接

> ```
> 内连接基于在 ON 子句中明确指定的列连接两个表。结果表将包含两个表中的所有属性，包括公共列。
> ```

### 左外连接

```mysql
  course natural left outer join prereq
```

出现在左边的元组一定会出现在结果之中，对于没有右边信息的用null填充

![image-20240513103326108](image-20240513103326108.png)

### 右外连接

```mysql
  course natural right outer join prereq
```

出现在右边关系中的元组一定会出现在结果之中，对于没有左边信息的用null填充

![image-20240513103334101](image-20240513103334101.png)

### 全外连接

```mysql
  course natural full outer join prereq
```

出现在两个关系的元组都会出现在结果中，无信息用null填充

![image-20240513103544065](image-20240513103544065.png)

### 连接条件

>只有满足条件的元组才能进行连接，并且条件中的属性在结果中会被重复保留

![image-20240513104154472](image-20240513104154472.png)

```mysql
course inner join prereq on course.course_id = prereq.course_id

```

![image-20240513103744413](image-20240513103744413.png)

```mysql
course left outer join prereq on course.course_id = prereq.course_id
```

![image-20240513104107848](image-20240513104107848.png)

![image-20240513104238809](image-20240513104238809.png)



![image-20240513104340385](image-20240513104340385.png)

## 视图

> A **view** provides a mechanism **to hide certain data from the view of certain users**. 
>
> Any relation that is not of the conceptual model but is made visible to a user as a “virtual relation” is called a **view**.

### 视图的定义

```sql
create view v as < query expression >
# where <query expression> is any legal SQL expression.  The view name is represented by v.
```

- 一旦视图被定义，那么这个视图的名字可以用来代指视图产生的**虚拟关系**
- 数据库系统存储的是与视图关系相关联的**查询表达式**
- 视图关系概念上包含了查询结果的元组但**不进行预先计算和存储**
- 视图一旦被创建，在被显示删除之前一直可用

```mysql
 create view faculty as
 select ID, name, dept_name
 from instructor
```

```mysql
# Find all instructors in the Biology department
select name
from faculty
where dept_name = 'Biology'
#Create a view of department salary totals
create view departments_total_salary( dept_name,total_salary) as 
				select dept_name, sum (salary)
                 from instructor
                 group by dept_name;

```

### 用视图定义视图



```mysql
create view physics_fall_2009 as
select course.course_id, sec_id, building, room_number
from course, section
where course.course_id = section.course_id  and course.dept_name = 'Physics'and section.semester = 'Fall' and section.year = '2009';

create view physics_fall_2009_watson as
select course_id, room_number
from physics_fall_2009
where building= 'Watson';
```

> - 若视图v1在定义的时候使用了视图v2，则v1直接依赖于v2
> - 若视图v1在定义的时候使用了视图v2，或者视图v1到视图v2之间存在依赖路径，则v1依赖于v2
> - A view relation *v* is said to be *recursive* if it depends on itself.

**判断闭包的方法**

>**repeat
>**  Find any view relation *v**i* in *e*1
>  Replace the view relation *v**i* by the expression defining *v**i* 
>  **until** no more view relations are present in *e*1

As long as the view definitions are not recursive, this loop will terminate

### 视图更新

```sql
#向视图中添加新的元组
insert into faculty values ('30765', 'Green', 'Music');
#This insertion must be represented by the insertion of the tuple
#			('30765', 'Green', 'Music', null)
#	into the instructor relation
```

**sql视图是可更新（插入 删除 更新），若满足下列条件**

> The **from** clause has only one database relation.
>
> The **select** clause contains only attribute names of the relation, and does not have any expressions, aggregates, or **distinct** specification.
>
> Any attribute not listed in the **select** clause can be set to null
>
> The query does not have a **group** **by** or **having** clause.

### 物化视图

> create a physical table containing all the tuples in the result of the query defining the view

**tips：**

- If relations used in the query are updated, the materialized view result becomes out of date
- Need to **maintain** the view, by updating the view whenever the underlying relations are updated.

- 视图是一种“虚关系”，实际查询时需要根据定义查询底层关系，当存在大量这样的查询时会有较高的成本。
- 某些数据库支持物化视图，像存储表一样将创建的视图关系“物化”存储在数据库中。 
- 物化视图的创建、修改与删除语法同视图类似，区别是多了关键字 **MATERIALIZED**



## 完整性约束

> 保护数据的一致性

**单个关系上的完整性约束**

> **not null ** 	非空

```sql
#Declare name and budget to be not null
name varchar(20) not null       
budget numeric(12,2) not null
```

> **primary key**		主码

既要非空又要保证唯一性

> **unique	**	唯一性

```sql
unique ( A1, A2, …, Am)
```

- **让A1,A2,..,Am，成为了超码**
- **声明了唯一性的属性允许为空**

> **check** (P), where P is a predicate

**关系中的每个元组都要满足谓词P**

```sql
#ensure that semester is one of fall, winter, spring or summer:
create table section (
    course_id varchar (8),
    sec_id varchar (8),
    semester varchar (6),
    year numeric (4,0),
    building varchar (15),
    room_number varchar (7),
    time slot id varchar (4), 
    primary key (course_id, sec_id, semester, year),
    check (semester in ('Fall', 'Winter', 'Spring', 'Summer'))
);
```

**引用完整性**

> - **保证引用关系中的给定属性集合的取值也在被引用关系的特定属性集的取值中出现**
> - **外码是引用完整性约束的一种形式，其中被引用的属性构成被引用关系的主码**
> - 至少要保证被引用关系的唯一性，要么主码约束要么唯一性约束

```sql
create table course (
course_id   char(5) primary key,
title varchar(20),
dept_name varchar(20) references department#dept_name是department的主码
)
```

**引用完整性上的级联操作**

```sql
create table course (
…
dept_name varchar(20),
foreign key (dept_name) references department
on delete cascade#如果被引用关系上的删除，更新操作违反了约束，那么就进行级联删除或者更新
on update cascade,
. . . 
)
on update cascade
on delete cascade
on update set null#置空值
on update set defualt#置缺省置
```

**复杂check语句**

> **复杂的check语句在我们希望保证数据的完整性是有用的，但开销十分巨大**

```sql
check (time_slot_id in (select time_slot_id from time_slot))
#section关系上定义约束
#why not use a foreign key here?   因为不是超码
```

上述语句不仅要在section更新时候进行计算，也要在time_slot发生更新的时候计算

## **断言**

> 谓词，表达了希望数据库总满足的一个条件

```sql
create assertion <assertion-name> check <predicate>;
#不被任何数据库支持
```

**创建断言的时候系统会检测其有效性，检测和维护有效性的开销很大，但触发器可以实现等价功能**

## 数据类型

![image-20240520195105693](image-20240520195105693.png)

## 创建索引

> **索引：一种数据结构，允许数据库系统高效地找到关系中具有该属性指定值的元组，而不扫描关系的所有元组**

```sql
create table student	
( ID varchar (5),
name varchar (20) not null,
dept_name varchar (20),
tot_cred numeric (3,0) default 0,
primary key (ID) )
create index studentID_index on student(ID)
---------------------------------------------------------------------------------
select * 
from  student
where  ID = ‘12345'
#can be executed by using the index to find the required record, without looking at all records of student
```

## 用户自定义类型



```sql
create type Dollars as numeric (12,2) final 

create table department
( dept_name varchar (20),
 building varchar (15),
 budget Dollars );
create type Pounds as numeric (12,2) final 
# Pounds和Dollars不是一种类型
```

## 域

![image-20240520195647678](image-20240520195647678.png)

## 大对象类型

![image-20240520195728022](image-20240520195728022.png)

## 授权

```sql
grant <privilege list>
on <relation name or view name> to <user list>
```

sql中的权限：

- **select：allows read access to** **relation,or** **the ability to query using the view**
- **insert:the ability to insert tuples**
- **update:** **the ability to update using the SQL update statement**
- **delete：the ability to delete tuples.**
- **all** **privileges：used as a short form for all the allowable privileges**

### 移除权限

```sql
revoke <privilege list>
on <relation name or view name> from <user list>
```

- 如果 **<revokee-list>**包含public那么全部的用户会失去权限，除了授权用户
- 如果相同的权限被不同的人授予给相同的用户两次，那么在被一次撤权后会保留权限。
- 所有依赖被撤除权限的权限也会被撤除

### 角色

```sql
create role instructor
grant instructor to Amit
# Privileges can be granted to roles:
grant select on takes to instructor
# Roles can be granted to users, as well as to other roles
create role teaching_assistant
grant teaching_assistant to instructor # Instructor inherits all privileges of teaching_assistant
```

### 视图的授权

```sql
create view geo_instructor as
( select *
 from instructor
 where dept_name = ’Geology’);
grant select on geo_instructor to  geo_staff

```

### 授权的转移

```sql
#允许被授权用户进行授权
grant select on department to Amit with grant option;
#级联收权，缺省
revoke select on department from Amit, Satoshi cascade;
#显示限定不级联收权
revoke select on department from Amit, Satoshi restrict;
#仅收回授权选项
revoke grant option for select on department from Amit, Satoshi restrict;
```

**一个用户具有权限等价于授权图中存在由根到用户节点的路径**

# 高级SQL

## 函数与过程

### 函数

```sql
#Define a function that, given the name of a department, returns the count of the number of instructors in that department.
create function dept_count (dept_name varchar(20))
returns integer
begin
declare d_count  integer;

select count (* ) into d_count
from instructor
where instructor.dept_name = dept_name

return d_count;
end
--------
select dept_name, budget
from department
where dept_count (dept_name ) > 12
```

![image-20240522090152312](image-20240522090152312.png)

### 存储过程

![image-20240522085957034](image-20240522085957034.png)

![image-20240522090006465](image-20240522090006465.png)

![image-20240522090059620](image-20240522090059620.png)

区别

- **存储过程和函数是事先经过编译并存储在数据库中的一段SQL语句的集合** 
- **存储过程和函数可以对一段代码进行封装，以便日后调用**
- **数据库中创建存储过程的语句为CREATE PROCEDURE，并通过CALL语句加存储过程名来调用存储过程**
- **数据库中创建函数的语句为CREATE FUNCTION，并通过函数名来调用函数**
- **存储过程和函数都用于提高数据库性能，减少频繁访问数据库和减少网络延迟等方式加速执行效率。**
- **函数：简单的计算型任务，例如字符串或日期拼接、返回单个值等。**
- **存储过程：复杂的业务逻辑、更新和删除相关操作。**
- **存储过程需要显式地被调用，并且可以包含各种复杂的控制结构和代码块。**

![image-20240522090240468](image-20240522090240468.png)

## 触发器

> 可以被系统自动执行、作为数据库修改的side effect 的语句

- **我们要指定触发器执行的条件和动作**

- **触发器事件可以是插入、删除、更新，其中更新可以限定到一个属性上 更新前后可以被引用**

  ```sql
  referencing old row as  :for deletes and updates
  referencing new row as  : for inserts and updates
  ```

```SQL
create trigger setnull_trigger before update of takes
referencing new row as nrow
for each row
when (nrow.grade = ‘ ‘)
begin atomic
	set nrow.grade = null;   
end;
```

```sql
create trigger credits_earned after update of takes on (grade)
referencing new row as nrow
referencing old row as orow
for each row
when nrow.grade <> ’F’ and nrow.grade is not null
	and (orow.grade = ’F’ or orow.grade is null)
begin atomic
update student
	set tot_cred= tot_cred + 
		(select credits
		from course
		where course.course_id= nrow.course_id)
		where student.id = nrow.id;
end;
```

![image-20240522091147745](image-20240522091147745.png)

![image-20240522090959333](image-20240522090959333.png)

![image-20240522091258072](image-20240522091258072.png)

![image-20240522091316867](image-20240522091316867.png)

## 闭包查询

```sql
with recursive rec_prereq(course_id, prereq_id) as (
	select course_id, prereq_id
	from prereq
	union
	select rec_prereq.course_id, prereq.prereq_id,
	from rec_rereq, prereq
	where rec_prereq.prereq_id = prereq.course_id
)
select ∗ 
from rec_prereq;
```

