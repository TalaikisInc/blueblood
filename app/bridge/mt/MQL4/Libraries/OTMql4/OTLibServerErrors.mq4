// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8; encoding: utf-8-dos -*-

#property copyright "Copyright 2009, OpenTrading"
#property link      "https://github.com/OpenTrading/"
#property library

//  One of the many fundamental defects of the Mql4 language
//  is that there is no Object Oriented error handling.
//
//  This leads to Mq4 returning hundreds of different errors
//  that are not grouped so that we can take actions based
//  on classes of errors.
//
//  We try to group the large number of errors into 9 groups
//  so that we can for example retry a trade when there is
//  some kind of network error.
//

#define OFLIB_OTHER_ERROR 0
#define OFLIB_BUSY_ERROR 1 // continuable - should retry
#define OFLIB_ORDER_ERROR 2
#define OFLIB_ACCOUNT_ERROR 3
#define OFLIB_NETWORK_ERROR 4
#define OFLIB_FATAL_ERROR 5
#define OFLIB_WINDOW_ERROR 6
#define OFLIB_FILE_ERROR 7
#define OFLIB_RUNTIME_ERROR 8

#include <stderror.mqh>

bool bOTLibServerErrorIsContinuable(int iErr) {
     int i;

     i = bOTLibServerErrorType(iErr);
     // Im not really sure what "commonerror" is (OFLIB_OTHER_ERROR)
     return(i == OFLIB_BUSY_ERROR || i == OFLIB_NETWORK_ERROR);
}

bool bOTLibServerErrorType(int iErr) {
    //  Group the errors returned from trade server
    //  so that we can take action based on classes of errors.
    switch(iErr) {
    case ERR_NO_ERROR: // 0
    return(OFLIB_OTHER_ERROR);
    case ERR_NO_RESULT: // 1
    return(OFLIB_OTHER_ERROR);
    case ERR_COMMON_ERROR: // 2
    return(OFLIB_OTHER_ERROR);

    case ERR_INVALID_TRADE_PARAMETERS: // 3
    return(OFLIB_ORDER_ERROR);

    case ERR_SERVER_BUSY: // 4
    return(OFLIB_BUSY_ERROR);

    case ERR_OLD_VERSION: // 5
    return(OFLIB_FATAL_ERROR);

    case ERR_NO_CONNECTION: // 6
    return(OFLIB_NETWORK_ERROR);

    case ERR_NOT_ENOUGH_RIGHTS: // 7
    case ERR_TOO_FREQUENT_REQUESTS: // 8
    case ERR_MALFUNCTIONAL_TRADE: // 9
    return(OFLIB_ORDER_ERROR); //? or retry?

    case ERR_ACCOUNT_DISABLED: // 64
    case ERR_INVALID_ACCOUNT: // 65
    return(OFLIB_ACCOUNT_ERROR);

    case ERR_TRADE_TIMEOUT: // 128
    return(OFLIB_NETWORK_ERROR);

    case ERR_INVALID_PRICE: // 129
    case ERR_INVALID_STOPS: // 130
    return(OFLIB_BUSY_ERROR);

    case ERR_INVALID_TRADE_VOLUME: // 131
    case ERR_MARKET_CLOSED: // 132
    case ERR_TRADE_DISABLED: // 133
    case ERR_NOT_ENOUGH_MONEY: // 134
    return(OFLIB_ORDER_ERROR);

    case ERR_PRICE_CHANGED: // 135
    return(OFLIB_BUSY_ERROR);

    case ERR_OFF_QUOTES: // 136
    case ERR_BROKER_BUSY: // 137
    case ERR_REQUOTE: // 138
    return(OFLIB_BUSY_ERROR);

    case ERR_ORDER_LOCKED: // 139
    return(OFLIB_BUSY_ERROR);

    case ERR_LONG_POSITIONS_ONLY_ALLOWED: // 140
    case ERR_TOO_MANY_REQUESTS: // 141
    case ERR_TRADE_MODIFY_DENIED: // 145
    return(OFLIB_ORDER_ERROR);

    case ERR_TRADE_CONTEXT_BUSY: // 146
    return(OFLIB_BUSY_ERROR);

    case ERR_TRADE_EXPIRATION_DENIED: // 147
    case ERR_TRADE_TOO_MANY_ORDERS: // 148
    return(OFLIB_ORDER_ERROR);

    //---- mql4 run time errors
    case ERR_NO_MQLERROR: // 4000
    case ERR_WRONG_FUNCTION_POINTER: // 4001
    case ERR_ARRAY_INDEX_OUT_OF_RANGE: // 4002
    case ERR_NO_MEMORY_FOR_CALL_STACK: // 4003
    case ERR_RECURSIVE_STACK_OVERFLOW: // 4004
    case ERR_NOT_ENOUGH_STACK_FOR_PARAM: // 4005
    case ERR_NO_MEMORY_FOR_PARAM_STRING: // 4006
    case ERR_NO_MEMORY_FOR_TEMP_STRING: // 4007
    case ERR_NOT_INITIALIZED_STRING: // 4008
    case ERR_NOT_INITIALIZED_ARRAYSTRING: // 4009
    case ERR_NO_MEMORY_FOR_ARRAYSTRING: // 4010
    case ERR_TOO_LONG_STRING: // 4011
    case ERR_REMAINDER_FROM_ZERO_DIVIDE: // 4012
    case ERR_ZERO_DIVIDE: // 4013
    case ERR_UNKNOWN_COMMAND: // 4014
    case ERR_WRONG_JUMP: // 4015
    case ERR_NOT_INITIALIZED_ARRAY: // 4016
    case ERR_DLL_CALLS_NOT_ALLOWED: // 4017
    case ERR_CANNOT_LOAD_LIBRARY: // 4018
    case ERR_CANNOT_CALL_FUNCTION: // 4019
    case ERR_EXTERNAL_CALLS_NOT_ALLOWED: // 4020
    case ERR_NO_MEMORY_FOR_RETURNED_STR: // 4021
    case ERR_SYSTEM_BUSY: // 4022
    case ERR_INVALID_FUNCTION_PARAMSCNT: // 4050
    case ERR_INVALID_FUNCTION_PARAMVALUE: // 4051
    case ERR_STRING_FUNCTION_INTERNAL: // 4052
    case ERR_SOME_ARRAY_ERROR: // 4053
    case ERR_INCORRECT_SERIESARRAY_USING: // 4054
    case ERR_CUSTOM_INDICATOR_ERROR: // 4055
    case ERR_INCOMPATIBLE_ARRAYS: // 4056
    case ERR_GLOBAL_VARIABLES_PROCESSING: // 4057
    case ERR_GLOBAL_VARIABLE_NOT_FOUND: // 4058
    case ERR_FUNC_NOT_ALLOWED_IN_TESTING: // 4059
    case ERR_FUNCTION_NOT_CONFIRMED: // 4060
    case ERR_SEND_MAIL_ERROR: // 4061
    case ERR_STRING_PARAMETER_EXPECTED: // 4062
    case ERR_INTEGER_PARAMETER_EXPECTED: // 4063
    case ERR_DOUBLE_PARAMETER_EXPECTED: // 4064
    case ERR_ARRAY_AS_PARAMETER_EXPECTED: // 4065
    case ERR_HISTORY_WILL_UPDATED: // 4066
    return(OFLIB_RUNTIME_ERROR);

    case ERR_TRADE_ERROR: // 4067
    return(OFLIB_BUSY_ERROR);

    case ERR_END_OF_FILE: // 4099
    case ERR_SOME_FILE_ERROR: // 4100
    case ERR_WRONG_FILE_NAME: // 4101
    case ERR_TOO_MANY_OPENED_FILES: // 4102
    case ERR_CANNOT_OPEN_FILE: // 4103
    case ERR_INCOMPATIBLE_FILEACCESS: // 4104
    return(OFLIB_FILE_ERROR);

    case ERR_NO_ORDER_SELECTED: // 4105
    case ERR_UNKNOWN_SYMBOL: // 4106
    case ERR_INVALID_PRICE_PARAM: // 4107
    case ERR_INVALID_TICKET: // 4108
    case ERR_TRADE_NOT_ALLOWED: // 4109
    case ERR_LONGS_NOT_ALLOWED: // 4110
    case ERR_SHORTS_NOT_ALLOWED: // 4111
    return(OFLIB_ORDER_ERROR);

    case ERR_OBJECT_ALREADY_EXISTS: // 4200
    case ERR_UNKNOWN_OBJECT_PROPERTY: // 4201
    case ERR_OBJECT_DOES_NOT_EXIST: // 4202
    case ERR_UNKNOWN_OBJECT_TYPE: // 4203
    case ERR_NO_OBJECT_NAME: // 4204
    case ERR_OBJECT_COORDINATES_ERROR: // 4205
    case ERR_NO_SPECIFIED_SUBWINDOW: // 4206
    case ERR_SOME_OBJECT_ERROR: // 4207
    return(OFLIB_WINDOW_ERROR);
    }
    return(OFLIB_OTHER_ERROR);
}
