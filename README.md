# webmap

## Install vue js

First Check if it's already installed

```shell
vue --version
```

- If not :

```shell
npm install -g @vue/cli
# OR
yarn global add @vue/cli
```

- If yes :

```shell
npm update -g @vue/cli
# OR
yarn global upgrade --latest @vue/cli
```

## Project setup

Copy the content of .env.example to your own .env

```shell
cp .env.example .env
```



##### If you'll re-push in this repository don't forget to param your .gitignor in adding  :

##### And to commit and push .gitignore first

```shell
.env
```



Install dependency

```shell
npm install
```

Compiles and hot-reloads for development

```
npm run serve
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
