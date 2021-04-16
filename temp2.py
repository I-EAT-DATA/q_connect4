if __name__ == "__main__":
    d = {'aKey': 'aVal', 'bKey': 'bVal'}
    print("d=", d)
    dl = [d] * 5 #[d, d, d, d]
    print("dl=", dl)
    d['aKey']='aNewKey'
    print("dl=", dl)
