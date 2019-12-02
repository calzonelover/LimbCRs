#ifndef PARSER
#define PARSER


class Parser {
    public:
        Parser();
        static std::string parseIntOrder(int _week, int range=3);

        template <typename T>
        static std::string parseDecimal(T val, int order);
};

#endif