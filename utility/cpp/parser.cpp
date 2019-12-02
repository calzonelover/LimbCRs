#include <stdio.h>
#include <stdlib.h>
#include <string>

#include "parser.h"

std::string Parser::parseIntOrder(int _week, int range){
    auto week = std::to_string(_week);
    while (week.size() < range){
        week = "0" + week;
    }
    return week;
}

template <typename T>
std::string Parser::parseDecimal(T val, int order){
    auto val_str = std::to_string(val);
    return val_str.substr(0, val_str.find(".")+order+1);
}
template std::string Parser::parseDecimal<float>(float, int);
template std::string Parser::parseDecimal<double>(double, int);