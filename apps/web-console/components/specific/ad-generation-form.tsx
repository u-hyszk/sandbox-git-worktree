'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Plus, X, Loader2, Sparkles } from 'lucide-react'
import { FormData } from '@/types'

interface AdGenerationFormProps {
  onSubmit: (data: FormData) => void
  isLoading: boolean
}

const toneOptions = [
  { value: 'professional', label: 'プロフェッショナル' },
  { value: 'casual', label: 'カジュアル' },
  { value: 'formal', label: 'フォーマル' },
  { value: 'friendly', label: 'フレンドリー' },
  { value: 'humorous', label: 'ユーモラス' },
] as const

export function AdGenerationForm({ onSubmit, isLoading }: AdGenerationFormProps) {
  const [formData, setFormData] = useState<FormData>({
    productName: '',
    targetAudience: '',
    appealPoints: [],
    tone: 'professional',
    numCopies: 3,
  })

  const [appealPointInput, setAppealPointInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const addAppealPoint = () => {
    if (appealPointInput.trim() && !formData.appealPoints.includes(appealPointInput.trim())) {
      setFormData(prev => ({
        ...prev,
        appealPoints: [...prev.appealPoints, appealPointInput.trim()]
      }))
      setAppealPointInput('')
    }
  }

  const removeAppealPoint = (index: number) => {
    setFormData(prev => ({
      ...prev,
      appealPoints: prev.appealPoints.filter((_, i) => i !== index)
    }))
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      addAppealPoint()
    }
  }

  const isFormValid = formData.productName && formData.targetAudience && formData.appealPoints.length > 0

  return (
    <Card className="animate-fade-in shadow-lg border-0 bg-gradient-to-br from-card to-card/80">
      <CardHeader className="space-y-3 pb-6">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 bg-gradient-to-br from-primary to-primary/60 rounded-xl flex items-center justify-center">
            <Sparkles className="h-5 w-5 text-primary-foreground" />
          </div>
          <div>
            <CardTitle className="text-2xl font-bold tracking-tight">広告文生成</CardTitle>
            <CardDescription className="text-base mt-1">
              商品・サービスの情報を入力して、AIによる広告文を生成しましょう
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="productName">商品・サービス名</Label>
            <Input
              id="productName"
              value={formData.productName}
              onChange={(e) => setFormData(prev => ({ ...prev, productName: e.target.value }))}
              placeholder="例: 最新型スマートウォッチ 'Watch X'"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="targetAudience">ターゲット層</Label>
            <Textarea
              id="targetAudience"
              value={formData.targetAudience}
              onChange={(e) => setFormData(prev => ({ ...prev, targetAudience: e.target.value }))}
              placeholder="例: 健康志向の20代〜40代のビジネスパーソン"
              rows={3}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="appealPoints">アピールポイント</Label>
            <div className="flex gap-2">
              <Input
                id="appealPoints"
                value={appealPointInput}
                onChange={(e) => setAppealPointInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="例: バッテリー持続時間5日間"
              />
              <Button type="button" onClick={addAppealPoint} variant="outline" size="sm">
                <Plus className="h-4 w-4 mr-1" />
                追加
              </Button>
            </div>
            {formData.appealPoints.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-3">
                {formData.appealPoints.map((point, index) => (
                  <Badge
                    key={index}
                    variant="secondary"
                    className="flex items-center gap-2 pl-3 pr-2 py-2 text-sm hover:bg-secondary/80 transition-colors"
                  >
                    <span>{point}</span>
                    <button
                      type="button"
                      onClick={() => removeAppealPoint(index)}
                      className="rounded-full p-0.5 hover:bg-background/50 transition-colors"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                ))}
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="tone">トーン</Label>
              <Select
                value={formData.tone}
                onValueChange={(value: FormData['tone']) => 
                  setFormData(prev => ({ ...prev, tone: value }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="トーンを選択" />
                </SelectTrigger>
                <SelectContent>
                  {toneOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="numCopies">生成数</Label>
              <Select
                value={formData.numCopies.toString()}
                onValueChange={(value) => 
                  setFormData(prev => ({ ...prev, numCopies: parseInt(value) }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="生成数を選択" />
                </SelectTrigger>
                <SelectContent>
                  {[1, 2, 3, 4, 5].map((num) => (
                    <SelectItem key={num} value={num.toString()}>
                      {num}個
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button 
            type="submit" 
            className="w-full h-12 text-base font-semibold" 
            disabled={!isFormValid || isLoading}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                生成中...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-5 w-5" />
                広告文を生成
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}