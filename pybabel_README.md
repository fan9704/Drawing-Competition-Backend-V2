# PyBabel README

---

## Getting Started

### Step.1 Create **translations** folder for i18n message

```shell
mkdir translations
```

### Step.2 Setup translation file

```shell
pybabel extract -o ./translations/messages.pot .
```

### Step.X Init language files

```shell
# For en_US
pybabel init -i translations/messages.pot -d translations -l en
# For zh_TW
pybabel init -i translations/messages.pot -d translations -l zh_TW
```

### Step.X Compile .po to .mo

compile the .po files into .mo files

```shell
pybabel compile -d translations
```

---

## Reference

1. [Medium - How to Add i18n to Your FastAPI App](https://medium.com/@amirm.lavasani/how-to-add-i18n-to-your-fastapi-app-b546f7d183bb)