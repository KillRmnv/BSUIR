#include "FileSystem.h"
//EOF=-1  FREE=-2

std::string getCurrentDate() {
    auto t = std::time(nullptr);
    auto tm = *std::localtime(&t);
    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y-%m-%d");
    return oss.str();
}
void FileSystem::Catalog::createFile(std::string name, std::string creationDate, std::string properties, int size) {
    if (size<1) {
        throw std::invalid_argument("File size must be greater than 0");
    }
            if (properties.size() != 2) {
                throw std::invalid_argument("properties should be 2 symbols in length but is " + properties.size());
            }
            files.push_back(File(name, creationDate, properties, fs.clasterTable.add(size / fs.clasterSize + 1, -1)));
        }

        void FileSystem::Catalog::deleteFile(std::string name) {
            for (int file = 0; file < files.size(); file++) {
                if (files[file].getName() == name) {
                    fs.clasterTable.free(files[file].getNumOfClaster(), -1);
                    files.erase(files.begin() + file);
                }
            }
        }

        File FileSystem::Catalog::copyFile(std::string name) {
            File buff;
            int amnt = 0;
            for (auto &file: files) {
                if (file.getName() == name && amnt == 0) {
                    amnt++;
                    buff = file;
                } else if (amnt != 0 && file.getName() == name + "(" + std::to_string(amnt) + ")") {
                    amnt++;
                    buff = file;
                }
            }
            if (amnt == 0)
                throw std::invalid_argument("File not found");
            if (fs.catalog.amntOfFreeSpace()<buff.getLenght()) {
                throw std::invalid_argument("Not enought free space");
            }
            int size = fs.clasterTable.countAmnt(buff.getNumOfClaster());
            File toCopy(name + "(" + std::to_string(amnt) + ")", getCurrentDate(), buff.getProperties(),
                        fs.clasterTable.add(size, -1));

            std::string content = readFile(buff.getName());
            files.push_back(toCopy);

            writeFile(toCopy.getName(), const_cast<char *>(content.c_str()), content.size(),
                      true);

            return toCopy;
        }

        void FileSystem::Catalog::writeFile(std::string name, void *data, size_t dataSize, bool rewrite) {
            std::vector<int> indexes;
                for (auto& file: files) {
                    if (file.getName() == name) {
                        if (file.getProperties()[1] == 'w') {
                            unsigned int start = 0, buff;
                            int amnt = 1;
                            indexes = fs.clasterTable.clasterIndexes(file.getNumOfClaster());
                            void *buffer = malloc(dataSize + fs.clasterSize);
                            if (!rewrite) {
                                amnt = fs.clasterTable.countAmnt(file.getNumOfClaster());
                                memcpy(buffer, fs.clasters[indexes[amnt - 1]].read(), fs.clasterSize);
                                //std::cout << static_cast<char *>(buffer) << "\n";
                                start = strlen(static_cast<char *>(buffer));
                            }
                            memcpy(static_cast<char *>(buffer) + start, data, dataSize);
                            static_cast<char *>(buffer)[start + dataSize] = '\0';
                            // std::cout<<static_cast<char*>(buffer)<<"\n";
                            // std::cout<<static_cast<char*>(data)<<"\n";

                            if (fs.clasterTable.countAmnt(file.getNumOfClaster()) * fs.clasterSize < dataSize && rewrite) {
                                file.setNumOfFirstClaster(fs.clasterTable.add(
                                    (dataSize - fs.clasterTable.countAmnt(file.getNumOfClaster()) * fs.clasterSize) / fs.
                                    clasterSize + 1,
                                    file.getNumOfClaster()));
                            } else if (!rewrite && fs.clasterSize - start < dataSize) {
                                file.setNumOfFirstClaster(fs.clasterTable.add((dataSize - start) / fs.clasterSize + 1,
                                                                              file.getNumOfClaster()));
                            }
                            indexes = fs.clasterTable.clasterIndexes(file.getNumOfClaster());
                            buff = start;
                            start = 0;
                            for (int i = amnt - 1; i < indexes.size() && start < dataSize + buff; i++) {
                                fs.clasters[indexes[i]].write(static_cast<char *>(buffer) + start, fs.clasterSize);
                                //fs.clasters[indexes[i]].setAllocation(true);
                               // std::cout << static_cast<char *>(buffer) + start << "\n";
                                start += fs.clasterSize;
                            }
                            if (rewrite) {
                                int amnt;
                                file.setLenght(dataSize);
                                if (dataSize % fs.clasterSize == 0) {
                                    amnt = dataSize / fs.clasterSize - 1;
                                } else {
                                    amnt = dataSize / fs.clasterSize;
                                }
                                fs.clasterTable.free(file.getNumOfClaster(), amnt);
                            } else
                                file.setLenght(file.getLenght() + dataSize);
                            //std::cout << static_cast<char *>(buffer) << "\n";

                            return;
                        } else
                            throw std::invalid_argument("File not for reading");
                    }
                }

        }

        std::string FileSystem::Catalog::readFile(std::string name) {
    std::vector<int> indexes;
    for (auto file: files) {
        if (file.getName() == name ) {
            if (file.getProperties()[0] == 'r') {
                indexes = fs.clasterTable.clasterIndexes(file.getNumOfClaster());


                int start = 0;
                std::vector<char> readData(fs.clasterTable.countAmnt(file.getNumOfClaster()) * fs.clasterSize,
                                           '\0');
                for (int i = 0; i < indexes.size(); i++) {
                    if (start>=file.getLenght()) {
                        return std::string(readData.begin(), readData.end()) + " ";
                    }

                    memcpy(readData.data() + start, fs.clasters[indexes[i]].read(), fs.clasterSize);
                    // std::cout<<static_cast<char*>(readData)+start<<"  sfgdhfjg\n";
                    start += fs.clasterSize;
                }
                return std::string(readData.begin(), readData.end());
            } else
                throw std::invalid_argument("File not for reading");
        }
    }
}

void FileSystem::allocate_memory(unsigned int size, unsigned int clasterSize) {
    if (clasterSize > (double) size * 0.1) {
        throw std::invalid_argument("Claster size is too big!");
    }
    int amnt = size / clasterSize;
    clasterTable.allocate(amnt);
    this->clasterSize = clasterSize;
    for (int i = 0; i < amnt; i++) {
        Claster claster(clasterSize); // Создаём постоянный объект
        clasters.push_back(claster);    // Копируем объект в вектор
    }
}

void FileSystem::DAMP() {
    printf("=== FAT Table ===\n");
    clasterTable.print();

    printf("=== Files in Catalog ===\n");
    auto &files = catalog.getFiles();
    if (files.empty()) {
        printf("No files in the catalog.\n");
        return;
    }

    for (auto &file: files) {
        printf("File: %s\n", file.getName().c_str());
        printf("  Creation Date: %s\n", file.getCreationDate().c_str());
        printf("  Properties: %s\n", file.getProperties().c_str());
        printf("  First Cluster: %d\n", file.getNumOfClaster());
        printf("  Content:\n");

        try {
            std::string content = catalog.readFile(file.getName());
            printf("    %s\n", content.c_str());
        } catch (const std::exception &e) {
            printf("    Error reading file: %s\n", e.what());
        }
    }
}

void Menu::display() {
    FileSystem fs;
    bool exit = false;

    while (!exit) {
        std::cout << "\n=== File System Menu ===\n";
        std::cout << "1. Allocate Memory\n";
        std::cout << "2. Create File\n";
        std::cout << "3. Delete File\n";
        std::cout << "4. Rewrite  File\n";
        std::cout << "5. Write to File\n";
        std::cout << "6. Read from File\n";
        std::cout << "7. Copy File\n";
        std::cout << "8. Display File System Info\n";
        std::cout << "0. Exit\n";
        std::cout << "Enter your choice: ";

        int choice;
        std::cin >> choice;
        if (choice != 1 && fs.size() == 0&&choice!=0) {
            std::cout << "YOU MUST ALLOCATE MEMORY FIRST" << std::endl;
            choice = -1;
        }
        try {
            switch (choice) {

                case 1: {
                    if (fs.size() == 0) {
                        unsigned int size, clasterSize;
                        std::cout << "Enter total memory size: ";
                        std::cin >> size;
                        std::cout << "Enter cluster size: ";
                        std::cin >> clasterSize;
                        fs.allocate_memory(size, clasterSize);
                        std::cout << "Memory allocated successfully.\n";
                        break;
                    } else {
                        std::cout << "already allocated memory" << std::endl;
                    }
                }
                case 2: {
                    std::string name, properties;

                    std::cout << "Enter file name: ";
                    std::cin >> name;
                    std::cout << "Enter file properties (rw, r-, -w): ";
                    std::cin >> properties;
                    fs.getCatalog().createFile(name, getCurrentDate(), properties, 1);
                    std::cout << "File created successfully.\n";
                    break;
                }
                case 3: {
                    std::string name;
                    std::cout << "Enter file name to delete: ";
                    std::cin >> name;
                    fs.getCatalog().deleteFile(name);
                    std::cout << "File deleted successfully.\n";
                    break;
                }
                case 4: {
                    std::string name, data;
                    std::cout << "Enter file name: ";
                    std::cin >> name;
                    std::cout << "Enter data to write: ";
                    std::cin.ignore();
                    std::getline(std::cin, data);
                    fs.getCatalog().writeFile(name,  const_cast<char *>(data.c_str()), data.size(), true);
                    std::cout << "Data written successfully.\n";
                    break;
                }
                case 5: {
                    std::string name, data;
                    std::cout << "Enter file name: ";
                    std::cin >> name;
                    std::cout << "Enter data to write: ";
                    std::cin.ignore();
                    std::getline(std::cin, data);
                    fs.getCatalog().writeFile(name, const_cast<char *>(data.c_str()), data.size(), false);
                    break;
                }
                case 6: {
                    std::string name;
                    std::cout << "Enter file name: ";
                    std::cin >> name;
                    std::string content = fs.getCatalog().readFile(name);
                    printf("    %s\n", content.c_str());
                    break;
                }
                case 7: {
                    std::string name;
                    std::cout << "Enter file name: ";
                    std::cin >> name;
                    fs.getCatalog().copyFile(name);
                    break;
                }
                case 8: {
                    fs.DAMP();
                    break;
                }
                case 0: {
                    exit = true;
                    std::cout << "Exiting...\n";
                    break;
                }
                default:
                    std::cout << "Invalid choice. Please try again.\n";
            }
        } catch (const std::exception &e) {
            std::cout << "Error: " << e.what() << "\n";
        }
    }
}
int FatTable::add(int amnt, int start) {
        int temp = start;
        if (start != -1) {
            while (table[temp] != -1) {
                temp = table[temp];
            }
        }
        int toReturn = -2;
        for (auto it = table.begin(); it != table.end() && amnt != 0; it++) {
                if (toReturn == -2&&it->second==-2) {
                    it->second = -1;
                    toReturn = it->first;
                    amnt--;
                    continue;
                } else if (toReturn == -2) {
                    continue;
                }
                    it->second = toReturn;

                toReturn = it->first;
                amnt--;
        }
        if (start != -1) {
            table[temp] = toReturn;
            return start;
        }
        return toReturn;
    }

    void FatTable::allocate(int amnt) {
        for (int i = 0; i < amnt; i++) {
            table[i] = -2;
        }
    }

    void FatTable::free(int index, int amnt) {
        int nextClaster;
        do {
            if (amnt < 0) {
                if (index==-2) {
                    break;
                }
                nextClaster = table[index];
                table[index] = -2;
                index = nextClaster;
            } else if (amnt > 0) {
                index = table[index];
                amnt--;
            } else {
                nextClaster = index;
                index = table[index];
                table[nextClaster] = -1;
                amnt--;
            }
        } while (index != -1);
    }

    void FatTable::print() {
        for (auto it = table.begin(); it != table.end(); it++) {
            printf("%d->%d\n", it->first, it->second);
        }
    }

    int FatTable::countAmnt(int start) {
        int amnt = 0;
        while (start != -1) {
            start = table[start];
            amnt++;
        }
        return amnt;
    }

    std::vector<int> FatTable::clasterIndexes(int start) {
        std::vector<int> indexes;
        while (start != -1) {
            indexes.push_back(start);
            start = table[start];
        }
        return indexes;
    }
    unsigned int FatTable::amntOfFreeSpace(unsigned int clusterSize) {
        unsigned int amnt = 0;
        for (auto it = table.begin(); it != table.end(); it++) {
            if (it->second == -2) {
                amnt++;
            }
        }
        return amnt*clusterSize;
    }

