## Intents

### Intent ID: smoke

**Грамматика:**

```

slots:
    var_smoke:
        source: $Smoke
        type: Smoke
root:
    .* $smoke .*

```

### Intent ID: sex

**Грамматика:**

```

slots:
    var_sex:
        source: $Sex
        type: Sex
root:
    .* $sex .*

```

### Intent ID: stud

**Грамматика:**

```

slots:
    var_stud:
        source: $Stud
        type: Stud
root:
    .* $stud .*

```

### Intent ID: choose_dom

**Грамматика:**

```

slots:
    var_dom:
        source: $Dom
        type: Dom
root:
    .* $choose_dom .*

```

### Intent ID: kyr

**Грамматика:**

```

slots:
    var_kyr:
        source: $Kyr
        type: Kyr
root:
    .* $kyr .*

```

### Intent ID: fio

**Грамматика:**

```

slots:
    slot_fio:
        source: $fio
        type: fio
root:
    .* $fio .*

$fio:
    $YANDEX.FIO

```

## Entities

```

entity Smoke:
    lemma: true
    values:
        yes_smoke:
            Курю
            Иногда
            Бывает
            Дымлю
            Немного
            Да
        no_smoke:
            Никогда не курил
            Не курю
            Против этого
            Не пробовал
            Нет

entity Sex:
    lemma: true
    values:
        male:
            Мужской пол
            Мужской
            Мужчина
            Мужик
            Парень
            Мальчик
            М
        female:
            Женский пол
            Женский
            Женщина
            Мужик
            Девушка
            Девочка
            Ж

entity Stud:
    lemma: true
    values:
        no_stud:
            Не студент
            Не учусь
            Учусь в школе
            Работаю
            Нет
        stud:
            Недавно начал
            Да
            Студент
            Учуcь
            Обучаюсь в университете
            Обучаюсь в университете

entity Dom:
    lemma: true
    values:
        ob:
            общежитие
            общага
        kvar:
            Квартира
        rod:
            Родители

entity Kyr:
    lemma: true
    values:
        cigarettes:
            сигареты
        vape:
            вейп
            парилка
        icos:
            айкос

```
