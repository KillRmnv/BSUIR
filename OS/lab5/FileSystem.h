
#ifndef FILESYSTEM_H
#define FILESYSTEM_H
#include <cstring>
#include<vector>
#include<string>
#include<map>
#include<stdexcept>
#include<iostream>
#include <ctime>
#include <sstream>
#include <iomanip>
std::string getCurrentDate();

class Menu {
public:
    void display();
};

class Claster {
private:
    void *memory;
    size_t size;

public:
    Claster() : memory(nullptr), size(0) {}

    Claster(size_t size) : size(size) {
        memory = malloc(size);
        if (!memory) {
            throw std::bad_alloc();
        }
    }

    Claster(const Claster &other) : size(other.size) {
        if (other.memory) {
            memory = malloc(size);
            if (!memory) {
                throw std::bad_alloc();
            }
            memcpy(memory, other.memory, size); 
        } else {
            memory = nullptr;
        }
    }

    Claster(Claster &&other) noexcept : memory(other.memory), size(other.size) {
        other.memory = nullptr; 
        other.size = 0;
    }

    Claster &operator=(const Claster &other) {
        if (this == &other) return *this;

        if (memory) {
            free(memory);
        }

        size = other.size;

        if (other.memory) {
            memory = malloc(size);
            if (!memory) {
                throw std::bad_alloc();
            }
            memcpy(memory, other.memory, size);
        } else {
            memory = nullptr;
        }

        return *this;
    }

    Claster &operator=(Claster &&other) noexcept {
        if (this == &other) return *this; 

        if (memory) {
            free(memory);
        }

        memory = other.memory;
        size = other.size;

        other.memory = nullptr;
        other.size = 0;

        return *this;
    }

    ~Claster() {
        if (memory) {
            free(memory);
            memory = nullptr;
        }
    }

    void *read() {
        return memory;
    }

    void write(void *data, size_t length) {
        if (length > size) {
            throw std::out_of_range("Data length exceeds allocated memory");
        }
        memcpy(memory, data, length);
    }
};

class File {
private:
    int numOfFirstClaster;
    std::string name;
    std::string creationDate;
    std::string properties;
    unsigned int length;

public:
    File() = default;

    void setNumOfFirstClaster(int numOfClaster) {
        numOfFirstClaster = numOfClaster;
    }

    void setLenght(unsigned int length) {
        this->length = length;
    }

    unsigned int getLenght() {
        return length;
    }

    File(std::string name, std::string creationDate, std::string properties, int num) {
        this->name = name;
        this->creationDate = creationDate;
        this->properties = properties;
        this->numOfFirstClaster = num;
        length = 0;
    }

    std::string &getName() {
        return name;
    }

    std::string getCreationDate() {
        return creationDate;
    }

    std::string &getProperties() {
        return properties;
    }

    void setProperties(std::string &properties) {
        this->properties = properties;
    }

    void setName(std::string &name) {
        this->name = name;
    }

    void setCreationDate(std::string &creationDate) {
        this->creationDate = creationDate;
    }

    int &getNumOfClaster() {
        return numOfFirstClaster;
    }
};

class FatTable {
private:
    std::map<int, int> table;

public:
    int add(int amnt, int start) ;

    void allocate(int amnt);

    void free(int index, int amnt) ;

    void print() ;

    int countAmnt(int start) ;

    std::vector<int> clasterIndexes(int start) ;
    unsigned int amntOfFreeSpace(unsigned int clusterSize) ;
};
class FileSystem {
private:
    unsigned int clasterSize;
    FatTable clasterTable;
    std::vector<Claster> clasters;

public:
    FileSystem() : catalog(*this) {
    }

    size_t size() {
        return clasters.size();
    }

    Menu menu;

    class Catalog {
    private:
        std::vector<File> files;
        FileSystem &fs;

    public:
        unsigned int amntOfFreeSpace() {
            unsigned int amnt = 0;
            for (auto& file:files) {
                amnt += file.getLenght();
            }
            return fs.clasterSize*fs.clasters.size()-amnt;
        }
        void addFile(File file) {
            files.push_back(file);
        }

        Catalog(FileSystem &file_system) : fs(file_system) {
        }

        Catalog(const Catalog &) = delete;

        Catalog &operator=(const Catalog &) = delete;

        void createFile(std::string name, std::string creationDate, std::string properties, int size) ;

        void deleteFile(std::string name) ;

        File copyFile(std::string name);

        void writeFile(std::string name, void *data, size_t dataSize, bool rewrite) ;

        std::string readFile(std::string name);

        std::vector<File> &getFiles() {
            return files;
        }

        explicit Catalog(const FileSystem &file_system);
    };

    void allocate_memory(unsigned int size, unsigned int clasterSize);

    void DAMP();

    Catalog &getCatalog() {
        return catalog;
    }

private:
    Catalog catalog;
};

#endif //FILESYSTEM_H
