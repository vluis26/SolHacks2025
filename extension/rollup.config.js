import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import polyfillNode from 'rollup-plugin-polyfill-node'
import replace from '@rollup/plugin-replace';
import dotenv from 'dotenv';

export default [
  {
    input: 'popup.js',
    output: {
      file: 'dist/popup.js',
      format: 'iife', 
      name: 'bundle',
      inlineDynamicImports: true
    },
    plugins: [
      replace({
        preventAssignment: true,
        'process.env.SUPABASE_URL': JSON.stringify(process.env.SUPABASE_URL),
        'process.env.SUPABASE_KEY': JSON.stringify(process.env.SUPABASE_KEY),
      }),
      resolve({
        browser: true,
        preferBuiltins: false
      }),
      commonjs(),
      polyfillNode()
    ]
  },
  {
    input: 'content.js',
    output: {
      file: 'dist/content.js',
      format: 'iife',
      name: 'contentBundle',
      inlineDynamicImports: true
    },
    plugins: [
      replace({
        preventAssignment: true,
        'process.env.SUPABASE_URL': JSON.stringify(process.env.SUPABASE_URL),
        'process.env.SUPABASE_KEY': JSON.stringify(process.env.SUPABASE_KEY),
      }),
      resolve({
        browser: true,
        preferBuiltins: false
      }),
      commonjs(),
      polyfillNode()
    ]
  },
  {
    input: 'background.js',
    output: {
      file: 'dist/background.js',
      format: 'iife',
      name: 'contentBundle',
      inlineDynamicImports: true
    },
    plugins: [
      replace({
        preventAssignment: true,
        'process.env.SUPABASE_URL': JSON.stringify(process.env.SUPABASE_URL),
        'process.env.SUPABASE_KEY': JSON.stringify(process.env.SUPABASE_KEY),
      }),
      resolve({
        browser: true,
        preferBuiltins: false
      }),
      commonjs(),
      polyfillNode()
    ]
  }
]
