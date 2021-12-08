// eslint-disable-next-line no-undef
module.exports = {
  'env': {
    'browser': true,
    'es6': true
  },
  'extends': [
    'eslint:recommended',
    'plugin:vue/essential'
  ],
  'globals': {
    'uni': true,
    'Atomics': 'readonly',
    'SharedArrayBuffer': 'readonly'
  },
  'parserOptions': {
    'ecmaVersion': 11,
    'sourceType': 'module'
  },
  'plugins': [
    'vue'
  ],
  'rules': {
    // 生命周期排序
    'vue/order-in-components': [
      'error',
      {
        order: [
          'el',
          'title',
          'name',
          'parent',
          'directives',
          'components',
          'extends',
          'mixins',
          'props',
          'data',
          'computed',
          'filters',
          'LIFECYCLE_HOOKS',
          'methods',
          'watch',
          ['template', 'render'],
          'errorCaptured'
        ]
      }
    ],
    'no-new-object': 2, // 禁止使用new Object()
    'no-self-compare': 2, // 不能比较自身
    'no-sequences': 0, // 禁止使用逗号运算符
    // 'camelcase': [1, { // 驼峰大小写
    // 	'properties': 'always'
    // }],
    'default-case': 2, // switch语句最后必须有default
    'eol-last': 2, // 文件以单一的换行符结束
    'no-extra-semi': 2, // 可以多余的冒号
    'semi': [2, 'never'], // 语句可以不需要分号结尾
    'semi-spacing': [2, {
      'before': false,
      'after': true
    }],
    'no-extra-bind': 2, // 禁止不必要的功能绑定
    'no-irregular-whitespace': 2, // 不允许不规则的空白
    // "eqeqeq": 1, // 必须使用全等
    'no-undef': 2, // 可以 有未定义的变量
    // 警告
    'no-extra-boolean-cast': 1, // 不必要的bool转换
    'no-extra-parens': 1, // 非必要的括号
    'no-empty': 1, // 块语句中的内容不能为空
    'no-use-before-define': [1, 'nofunc'], // 未定义前不能使用
    'complexity': [1, 18], // 循环复杂度
    // 'flow-vars/use-flow-type': 1,
    // 错误
    'comma-dangle': [2, 'never'], // 对象字面量项尾不能有逗号
    'no-debugger': 1, // 禁止使用debugger
    'no-constant-condition': 2, // 禁止在条件中使用常量表达式 if(true) if(1)
    'no-dupe-args': 2, // 函数参数不能重复
    'no-dupe-keys': 2, // 在创建对象字面量时不允许键重复 {a:1,a:1}
    'no-duplicate-case': 2, // switch中的case标签不能重复
    'no-empty-character-class': 2, // 正则表达式中的[]内容不能为空
    'no-invalid-regexp': 2, // 禁止无效的正则表达式
    'no-func-assign': 2, // 禁止重复的函数声明
    'valid-typeof': 2, // 必须使用合法的typeof的值
    'no-unreachable': 2, // 不能有无法执行的代码
    'no-unexpected-multiline': 2, // 避免多行表达式
    'no-sparse-arrays': 2, // 禁止稀疏数组， [1,,2]
    'no-shadow-restricted-names': 2, // 严格模式中规定的限制标识符不能作为声明时的变量名使用
    'no-cond-assign': 2, // 禁止在条件表达式中使用赋值语句
    'no-native-reassign': 2, // 不能重写native对象
    'no-else-return': 1, // 如果if语句里面有return,后面不能跟else语句
    'no-multi-spaces': 2, // 不能用多余的空格
    'key-spacing': [1, { // 对象字面量中冒号的前后空格
      'beforeColon': false,
      'afterColon': true
    }],
    'no-unsafe-finally': 2,
    'no-unused-vars': [2, {
      'vars': 'all',
      'args': 'none'
    }],
    'no-useless-call': 2,
    'no-useless-computed-key': 1,
    'no-useless-constructor': 2,
    'no-useless-escape': 0,
    'no-whitespace-before-property': 2,
    'no-with': 2,
    'one-var': [2, {
      'initialized': 'never'
    }],
    'operator-linebreak': [2, 'after', {
      'overrides': {
        '?': 'before',
        ':': 'before'
      }
    }],
    'padded-blocks': [2, 'never'],
    'quotes': [2, 'single', {
      'avoidEscape': true,
      'allowTemplateLiterals': true
    }],
    'space-before-blocks': [2, 'always'],
    'space-before-function-paren': [2, 'never'], // 函数空格问题
    'space-in-parens': [2, 'never'],
    'space-infix-ops': 2,
    'space-unary-ops': [2, {
      'words': true,
      'nonwords': false
    }],
    'spaced-comment': [2, 'always', {
      'markers': ['global', 'globals', 'eslint', 'eslint-disable', '*package', '!', ',']
    }],
    'template-curly-spacing': [2, 'never'],
    'use-isnan': 2,
    'wrap-iife': [2, 'any'],
    'yield-star-spacing': [2, 'both'],
    'yoda': [2, 'never'],
    'prefer-const': 2
  }
}
