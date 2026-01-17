## 引用计数

### 环状双向链表 refchain

在 Python 程序中创建的任何对象都会被放到 refchain 链表中，当创建一个 Python 对象时，内部实际上创建了一些基本的数据：

- 上一个对象
- 下一个对象
- 类型
- 引用个数
- 值
- 对于列表等类型，也会创建值用于存储列表的长度

在 C 源码中体现如下：

```c
#define PyObject_HEAD		PyObject ob_base;
#define PyObject_VAR_HEAD		PyVarObject ob_base;

// 宏定义，包含：上一个、下一个、用于构造双向链表用
#define _PyObject_HEAD_EXTRA
	struct _object *_ob_next;
	struct _object *_ob_prev;

typedef struct _object {
    _PyObject_HEAD_EXTRA 
    Py_ssize_t ob_refcnt; // 引用计数器
    struct _typeobject *ob_type; // 数据类型
} PyObject;

//list、tuple、dict..
typedef struct {
    PyObject ob_base;  // PyObject 对象
    Py_ssize_t ob_size;  // 元素个数
} PyVarObject;

//float
typedef struct {
    PyObject_HEAD
    double ob_fval;
} PyFloatObject;
```

比如对于下面这段 Python 代码：

```python
data = 3.14
```

其内部会创建：

```
_ob_next = refchain 中的下一个对象
	_ob_prev = refchain 中的下一个对象
	ob_refcnt = 1
	ob_type = float
	ob_fval = 3.14
```

### 引用计数器

在 Python 程序运行时，会根据数据类型的不同找到其对应的结构体，根据结构体中的字段来进行创建相关的数据，然后将对象添加到 refchain 双向链表中。

在 C 源码中有两个关键的结构体：PyObject、PyVarObject。

每个对象中都有 ob_refcnt，即引用计数器，默认值为 1，当有其他变量引用对象时，引用计数器就会发生变化。

当一个对象的引用计数器为 0 时，意味着没有人再使用这个对象了，这个对象就会被垃圾回收，流程如下：

1. 把对象从 refchain 链表中移除
2. 将对象销毁，内存归还

注：`del` 语句实际上就是在对引用计数器做`-1` 操作。

## 垃圾回收器

### 循环引用

大部分时候，引用计数可以很好的清理内存，但是遇到循环引用，就无法处理了，比如：

```python
x = []
x.append(x)
del x
```

此时，因为 x 的的引用计数还在，导致它所指向的内存无法清理。

为此，Python 引入了垃圾回收器机制，在 cpython 内部，会维护一个新的链表，用于存放可能存在循环引用的对象，比如 list, dict, set, 以及非空的 tuple 等。当达到一定条件后，会去遍历每个元素，检查是否有循环引用，如果有，则让双方的引用计数 -1，如果是 0 则进行回收。

整形、浮点数、布尔值、NoneType 不会被标记。

可以通过 `gc.is_tracked` 方法来判断对象是否被加入到该列表，比如：

```python
>>> import gc
>>> x = ()  # 空元组不会被追踪，因为它不可变，也不存在循环引用>>> gc.is_tracked (x)
False
>>> 
>>> x = (1,)  # 非空元组会被追踪
>>> gc.is_tracked (x)
True
```

### 分代回收

对循环引用的清理也引发了两个问题：

1. 什么时候扫描？
2. 扫描代价较大（对子孙元素都要进行扫描），单次扫描耗时久。

对此，Python 使用了分代回收的机制。将可能存在循环引用的对象维护成 3 个链表：

- 0 代，个数达到 2000 个扫描一次，结束后，如果有存活的对象，则移动到下一代，即 1 代
- 1 代，0 代扫描 10 次，1 代扫描 1 次，结束后，如果有存活的对象，则移动到下一代，即 2 代
- 2 代，1 代扫描 10 次，2 代扫描 1 次

注意，老一代扫描时，也会将年轻代并入一起扫描。

可以使用 gc 模块来获取阈值或手动触发垃圾回收：

```python
>>> gc.get_threshold ()  # 获取分代触发的阈值
(2000, 10, 10)
>>> gc.get_count ()  # 获取各代的数量
(879, 12, 0)
>>> gc.collect (0)  # 手动回收 0 代，返回被回收的对象数量
769
>>> gc.collect ()  # 如果不指定，默认为 2 代
```

## 缓存

1. 池（int）
   
   为了避免重复的创建和销毁一些对象，维护池。
   
   ```python
   >>> a1 = 1
   >>> a2 = 1
   >>> id(a1)
   140713557615440
   >>> id(a2)
   140713557615440
   ```
2. free_list（float/list/tuple/dict）
   
   当一个对象的引用计数为 0 时，内部不会直接回收，而是将对象添加到 free_list 中当缓存，以后再去创建对象时，不再重新开辟内存，而是直接使用 free_list。
   
   ```python
   # 开辟新的内存
   v1 = 3.14
   
   # 将对象添加到 free_list 中
   del v1
   
   # 去 free_list 中获取对象，并将对象内存数据初始化
   v2 = 999
   ```

## 参考

1. [python 垃圾回收机制刨析](https://pythonav.com/wiki/detail/6/88/)