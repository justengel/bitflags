

def test_int_from_bits():
    from bitflags import int_from_bits

    value = int_from_bits(0, 2)  # 101
    assert value == 5

    value = int_from_bits(0, 1, 2)
    assert value == 7


def test_case_types():
    from bitflags import to_snake_case, toCamelCase, to_keep_case
    expected = [
        # Input, snake_case, camelCase, keep case
        ('CamelCase', 'camel_case', 'camelCase', 'CamelCase'),
        ('camelCamelCase', 'camel_camel_case', 'camelCamelCase', 'camelCamelCase'),
        ('Camel2Camel2Case', 'camel_2_camel_2_case', 'camel2Camel2Case', 'Camel2Camel2Case'),
        ('getHTTPResponseCode', 'get_http_response_code', 'getHttpResponseCode', 'getHTTPResponseCode'),
        ('get200HTTPResponseCode', 'get_200_http_response_code', 'get200HttpResponseCode', 'get200HTTPResponseCode'),
        ('getHTTP200ResponseCode', 'get_http_200_response_code', 'getHttp200ResponseCode', 'getHTTP200ResponseCode'),
        ('HTTPResponseCode', 'http_response_code', 'httpResponseCode', 'HTTPResponseCode'),
        ('ResponseHTTP', 'response_http', 'responseHttp', 'ResponseHTTP'),
        ('ResponseHTTP2', 'response_http_2', 'responseHttp2', 'ResponseHTTP2'),
        ('Fun?!awesome', 'fun_awesome', 'funAwesome', 'Fun_awesome'),
        ('Fun?!Awesome', 'fun_awesome', 'funAwesome', 'Fun_Awesome'),
        ('10CoolDudes', 'cool_dudes', 'coolDudes', 'CoolDudes'),
        ('20coolDudes', 'cool_dudes', 'coolDudes', 'coolDudes'),
        ('flag1', 'flag_1', 'flag1', 'flag1'),
    ]
    for input, snake, camel, keep in expected:
        assert snake == to_snake_case(input), f"Snake case failed for {input} => {snake}"
        assert camel == toCamelCase(input), f"Camel case failed for {input} => {camel}"
        assert keep == to_keep_case(input), f"Keep case failed for {input} => {keep}"


if __name__ == '__main__':
    test_int_from_bits()
    test_case_types()
    print('All tests passed successfully!')
