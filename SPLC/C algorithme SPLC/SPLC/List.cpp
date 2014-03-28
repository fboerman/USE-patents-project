//SPLC analyses
//For USE Patents&Standards course
//By Frank Boerman Tue 2014(c)
//cpp file for List class
//This class imitates a python list functionality to easily port my python SPLC algorithm

#include "List.h"

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
	_List = new T[len + 1];
	//copy over the old to new list
	for (int i = 0; i < _len; i++)
	{
		_list[i] = old_list[i];
	}
	//put the new item in
	_list[_len] = item;
	//update lenght variable
	_len++;
	//delete the old one
	delete[] old_list;
}

template<typename T> void List<T>::pop()
{

}

template<typename T> T List<T>::operator[](int i)
{

}