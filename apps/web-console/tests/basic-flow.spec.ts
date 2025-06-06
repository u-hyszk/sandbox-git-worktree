import { test, expect } from '@playwright/test'

test('basic navigation and form visibility', async ({ page }) => {
  await page.goto('/')

  await expect(page.locator('h1')).toContainText('AI広告文生成サービス')
  
  await expect(page.locator('h3')).toContainText('広告文生成')
  
  await expect(page.getByLabel('商品・サービス名')).toBeVisible()
  await expect(page.getByLabel('ターゲット層')).toBeVisible()
  await expect(page.getByLabel('アピールポイント')).toBeVisible()
})