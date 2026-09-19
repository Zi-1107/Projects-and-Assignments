#ifndef CONTAINER
#define CONTAINER

#include <iostream>
using namespace std;

template <typename T>
class Container {
private:
    T* list;
    int length;
    int size;

public:
    Container(int s) {
        if (s <= 0) {
            list = nullptr;
            length = 0;
            size = 0;
            cout << "Invalid container size" << endl;
        }
        else {
            list = new T[s];
            length = 0;
            size = s;
        }
    }

    ~Container() {
        delete[] list;
    }


    int getLength() const { return length; }
    int getSize() const { return size; }

    bool isEmpty() const { return length == 0; }
    bool isFull() const { return length == size; }

    void addItem(T item) {
        if (isFull()) {
            cout << "The Container is Full, unable to add new item" << endl;
        }
        else {
            list[length] = item;
            length++;
            cout << item << " was added to the container..." << endl;
        }
    }

    void print() {
        if (isEmpty()) {
            cout << "Container is empty" << endl;
        }
        else {
            cout << "The Container has: " << endl;
            for (int i = 0; i < length; i++) {
                cout << "Item " << (i + 1) << " : " << list[i] << endl;
            }
        }
    }

    bool searchItem(T item) const {
        for (int i = 0; i < length; i++) {
            if (list[i] == item) {
                return true;
            }
        }
        return false;
    }

    void removeItem(T item) {
        int index = -1;
        for (int i = 0; i < length; i++) {
            if (list[i] == item) {
                index = i;
                break;
            }
        }

        if (index == -1) {
            cout << "Item not found" << endl;
        }
        else {
            for (int i = index; i < length - 1; i++) {
                list[i] = list[i + 1];
            }
            length--;
            cout << item << " was removed" << endl;
        }
    }

    void updateItem(T oldItem, T newItem) {
        for (int i = 0; i < length; i++) {
            if (list[i] == oldItem) {
                list[i] = newItem;
                cout << oldItem << " was updated to " << newItem << endl;
                break;
            }
        }
    }

};

#endif