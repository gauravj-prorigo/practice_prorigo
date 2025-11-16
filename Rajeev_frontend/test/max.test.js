// test/max.test.js
import { describe, it, expect } from 'vitest'
import { max } from '../utils/max'

describe('max util', () => {
  it('returns the greater value', () => {
    expect(max(10, 5)).toBe(10)
  })
})
