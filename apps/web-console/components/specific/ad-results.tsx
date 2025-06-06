'use client'

import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Copy, RefreshCw, CheckCircle, TrendingUp, Target, MessageSquare, Star } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { GeneratedAdCopy } from '@/types'

interface AdResultsProps {
  results: GeneratedAdCopy[]
  onReset: () => void
}

export function AdResults({ results, onReset }: AdResultsProps) {
  const [copiedIndex, setCopiedIndex] = React.useState<number | null>(null)

  const copyToClipboard = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedIndex(index)
      setTimeout(() => setCopiedIndex(null), 2000)
    } catch (err) {
      console.error('コピーに失敗しました:', err)
    }
  }

  const formatScore = (score?: number) => {
    if (score === undefined) return 'N/A'
    return `${Math.round(score * 100)}%`
  }

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h2 className="text-3xl font-bold tracking-tight">生成結果</h2>
          <div className="flex items-center gap-2">
            <Badge variant="secondary" className="text-sm">
              <Star className="h-3 w-3 mr-1" />
              {results.length}個の広告文
            </Badge>
            <span className="text-muted-foreground text-sm">が生成されました</span>
          </div>
        </div>
        <Button onClick={onReset} variant="outline" className="flex items-center gap-2 h-10">
          <RefreshCw className="h-4 w-4" />
          新しく生成
        </Button>
      </div>

      <div className="grid gap-6">
        {results.map((result, index) => (
          <Card key={index} className="relative animate-slide-up shadow-lg border-0 bg-gradient-to-br from-card to-card/80 hover:shadow-xl transition-all duration-300" style={{animationDelay: `${index * 100}ms`}}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg">広告文 {index + 1}</CardTitle>
                  {result.headline && (
                    <CardDescription className="mt-2 font-medium text-base">
                      {result.headline}
                    </CardDescription>
                  )}
                </div>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => copyToClipboard(result.copyText, index)}
                  className="shrink-0 relative"
                  title="クリップボードにコピー"
                >
                  {copiedIndex === index ? (
                    <CheckCircle className="h-4 w-4 text-green-500" />
                  ) : (
                    <Copy className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <MessageSquare className="h-4 w-4 text-muted-foreground" />
                  <h4 className="font-medium">本文</h4>
                </div>
                <div className="bg-gradient-to-r from-muted/50 to-muted/30 p-4 rounded-lg border">
                  <p className="text-sm leading-relaxed text-foreground/90">
                    {result.copyText}
                  </p>
                </div>
              </div>

              {result.callToAction && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-primary" />
                    <h4 className="font-medium">行動喚起</h4>
                  </div>
                  <div className="bg-gradient-to-r from-primary/10 to-primary/5 border border-primary/20 p-4 rounded-lg">
                    <p className="text-sm text-primary font-medium">
                      {result.callToAction}
                    </p>
                  </div>
                </div>
              )}

              {result.evaluation && (
                <div className="border-t pt-6 space-y-4">
                  <div className="flex items-center gap-2">
                    <Target className="h-4 w-4 text-muted-foreground" />
                    <h4 className="font-medium">評価</h4>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                        <span className="text-sm font-medium">関連性スコア</span>
                        <Badge variant="outline" className="font-mono">
                          {formatScore(result.evaluation.relevanceScore)}
                        </Badge>
                      </div>
                      <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                        <span className="text-sm font-medium">創造性スコア</span>
                        <Badge variant="outline" className="font-mono">
                          {formatScore(result.evaluation.creativityScore)}
                        </Badge>
                      </div>
                    </div>
                    {result.evaluation.targetAudienceAppeal && (
                      <div className="space-y-3">
                        <div className="flex items-center gap-2">
                          <Target className="h-4 w-4 text-primary" />
                          <span className="text-sm font-medium">ターゲット層への響き</span>
                        </div>
                        <div className="bg-muted/30 p-3 rounded-lg border-l-4 border-primary/30">
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            {result.evaluation.targetAudienceAppeal}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}