# DPLL sat solver
Нужно реализовать свой SAT-решатель на основе алгоритма DPLL.

Можно запустить тесты локально, вызвав `python solver_test.py`.

Можно запустить проверку для определенного файла `python3 solver.py`
Далее увидим: `Print cnf file path:` после чего необходимо указать файл

## Выбранные тесты
### SAT
- **empty.cnf** - крайний случай - нет дизъюнктов
- **only-select.cnf** - полностью отсутствует unit-propagation
- **unit-propogation.cnf** - unit-propagation хватает чтобы разобрать все
- **only-pure.cnf** - идем по чистым переменным
- **3cnf-8-65_2.cnf** - неправильно отгадали и пришлось дважды вернуться
    - нет литералов одной полярности
    - думаем что 1
        - думаем что 5
            - думаем что 4
                - одиночный -2
                - одиночный 8
                - одиночный 6
                - противоречие (7 , -7)
            - думаем что -4
                - противоречие (-8 и 8)
    - думаем что -1
        - думаем что -3
            - одиночный -5
            - одиночный 4
            - одиночный -2
            - одиночный -7
            - одиночный -8
            - одиночный 6

### UNSAT
- **false.cnf** - крайний случай - пустой дизъюнкт
- **sat5.cnf** - полностью отсутствует unit-propagation
- **unit-propogation.cnf** - unit-propagation хватает чтобы разобрать все
- **rivest-unsat.cnf** - короткий пример с unit-propagation и выбором переменной
- **only-pure.cnf** - идем по чистым переменным и в конце получаем unsat