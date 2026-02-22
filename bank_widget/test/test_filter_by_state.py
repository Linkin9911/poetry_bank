if __name__ == '__main__':
    data = [
        {'state': 'EXECUTED', 'date': '2023-01-01'},
        {'state': 'CANCELED', 'date': '2023-01-02'}
    ]
    print(filter_by_state(data))
    print(sort_by_date(data))