import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import polyfillNode from 'rollup-plugin-polyfill-node'

export default {
  input: 'popup.js',
  output: {
    file: 'dist/popup.js',
    format: 'iife', 
    name: 'bundle',
    inlineDynamicImports: true
  },
  plugins: [
    resolve({
      browser: true,
      preferBuiltins: false
    }),
    commonjs(),
    polyfillNode()
  ]
}
