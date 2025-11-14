# -*- coding: utf-8 -*-
"""
hangulpy v1.3.0 Quickstart Examples
==================================

This file demonstrates the key features of hangulpy v1.3.0.
"""

from hangulpy import (
    # Josa (Particles)
    josa,
    # Search functions
    hangul_contains,
    hangul_search,
    HangulSearcher,
    # Character properties
    is_complete_hangul,
    get_hangul_components,
    # Assembly/Disassembly
    split_syllables,
    join_jamos,
    # Romanization
    romanize,
)


def main() -> None:
    print("=" * 60)
    print("hangulpy v1.3.0 - Quickstart Examples")
    print("=" * 60)

    # 1. Josa (Particles)
    print("\n1. Josa (Particles)")
    print("-" * 40)
    print(f"��� + ��/�� = {josa('���', '��/��')}")
    print(f"å + ��/�� = {josa('å', '��/��')}")
    print(f"1 + ��/�� = {josa('1', '��/��')}")

    # 2. Search Functions
    print("\n2. Search Functions")
    print("-" * 40)
    print(f"'���'�� '��' ����? {hangul_contains('���', '��')}")
    print(f"'����� ���ִ�'���� '��' ��ġ: {hangul_search('����� ���ִ�', '��')}")

    # HangulSearcher for repeated searches
    searcher = HangulSearcher("��")
    print(f"\nSearcher('��')�� �˻�:")
    print(f"  '������' �˻�: {searcher.search('������')}")
    print(f"  '�ٳ���' �˻�: {searcher.search('�ٳ���')}")

    # 3. Character Properties
    print("\n3. Character Properties")
    print("-" * 40)
    print(f"'��'�� �ϼ���? {is_complete_hangul('��')}")
    print(f"'��'�� �ϼ���? {is_complete_hangul('��')}")

    components = get_hangul_components("��")
    if components is not None:
        cho, jung, jong = components
        print(f"'��'�� ����: �ʼ�={cho}, �߼�={jung}, ����={jong}")

    # 4. Assembly/Disassembly
    print("\n4. Assembly/Disassembly")
    print("-" * 40)
    jamos = split_syllables("�ѱ�")
    print(f"'�ѱ�' ����: {jamos}")

    assembled = join_jamos(["��", "��", "��"])
    print(f"['��', '��', '��'] ����: {assembled}")

    # 5. Romanization
    print("\n5. Romanization")
    print("-" * 40)
    print(f"'�ѱ�' �� Revised: {romanize('�ѱ�', 'revised')}")
    print(f"'�ѱ�' �� Yale: {romanize('�ѱ�', 'yale')}")
    print(f"'�ȳ��ϼ���' �� Revised: {romanize('�ȳ��ϼ���', 'revised')}")

    # 6. Real-world Example: Auto-complete Search
    print("\n6. Real-world Example: Auto-complete Search")
    print("-" * 40)
    items = ["���", "����", "����", "�ٳ���", "������"]
    query = "��"
    searcher = HangulSearcher(query)
    results = [item for item in items if searcher.search(item)]
    print(f"'{query}' �˻� ���: {results}")

    # 7. Real-world Example: Dynamic Sentence Building
    print("\n7. Real-world Example: Dynamic Sentence Building")
    print("-" * 40)
    fruits = ["���", "�ٳ���", "������"]
    for fruit in fruits:
        sentence = f"{fruit}{josa(fruit, '��/��')} �Ծ����ϴ�."
        print(f"  {sentence}")

    print("\n" + "=" * 60)
    print("For more examples, see: https://wiki.uiharu.dev/w/hangulpy")
    print("=" * 60)


if __name__ == "__main__":
    main()

