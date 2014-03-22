//SPLC analyses
//For USE Patents&Standards course
//By Frank Boerman Tue 2014(c)
//Header file for List class
//This class imitates a python list functionality to easily port my python SPLC algorithm

#ifndef LIST_H
#define LIST_H

#include <string>

template<typename T> class List
{
public:
	List();//initializes the list with no items
	List(T item); //initializes the list with 1 item
	~List();

	//searches for given item and gives true if found
	bool Search(T item);
	//get string value from list
	std::string Get_String(int i);
	//get int value from list
	int Get_Int(int i);
	//get lenght of list
	int len();
	//append item to list
	void append(T item);
	//remove last item in list
	void pop();
	//set an item
	void Set(int i, T item);

private:
	T* _List; //the internal array to store the list
	int _len; //current length of list
};

template<typename T> List<T>::List(T item)
{
	List();
	append(item);
}

template<typename T> List<T>::List()
{
	_len = 0;

}

template<typename T> List<T>::~List()
{
	if (_len > 0)
	{
		delete[] _List;
	}
}

template<typename T> void List<T>::Set(int i, T item)
{
	_List[i] = item;
}

template<typename T> int List<T>::len()
{
	return _len;
}

template<typename T> void List<T>::append(T item)
{
	//copy list
	T * old_list = _List;
	//intiliaze new size
	_List = new T[_len + 1];
	//copy over the old to new list
	for (int i = 0; i < _len; i++)
	{
		_List[i] = old_list[i];
	}
	//put the new item in
	_List[_len] = item;
	//update lenght variable
	_len++;
	//delete the old one
	delete[] old_list;
}

template<typename T> void List<T>::pop()
{
	//copy list
	T * old_list = _List;
	//intiliaze new size
	_List = new T[_len - 1];
	//update the new length
	_len--;
	//copy over the old to new list
	for (int i = 0; i < _len; i++)
	{
		_List[i] = old_list[i];
	}
	//delete the old list
	delete old_list;
}

template<typename T> std::string List<T>::Get_String(int i)
{
	if (i >= _len)
	{
		return nullptr;
	}
	return _List[i];
}

template<typename T> int List<T>::Get_Int(int i)
{
	return _List[i];
}

template<typename T> bool List<T>::Search(T item)
{
	for (int i = 0; i < _len; i++)
	{
		if (_List[i] == item)
		{
			return true;
		}
	}
	return false;
}

#endif