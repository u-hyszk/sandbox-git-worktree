import { AdGenerationForm } from '@/components/specific/ad-generation-form'
import { AdResults } from '@/components/specific/ad-results'
import { ErrorDisplay } from '@/components/common/error-display'
import { useAdGeneration } from '@/lib/hooks'
import { FormData } from '@/types'

function App() {
  const { isLoading, error, results, generateAdCopy, reset } = useAdGeneration()

  const handleFormSubmit = async (formData: FormData) => {
    await generateAdCopy({
      productName: formData.productName,
      targetAudience: formData.targetAudience,
      appealPoints: formData.appealPoints,
      tone: formData.tone,
      numCopies: formData.numCopies,
    })
  }

  const handleRetry = () => {
    reset()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20 font-sans antialiased">
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 bg-gradient-to-br from-primary to-primary/60 rounded-lg flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">AI</span>
            </div>
            <h1 className="text-2xl font-bold text-foreground tracking-tight">
              AI広告文生成サービス
            </h1>
          </div>
        </div>
      </header>
      <main className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="space-y-8">
          {!results && !error && (
            <AdGenerationForm onSubmit={handleFormSubmit} isLoading={isLoading} />
          )}

          {error && (
            <ErrorDisplay error={error} onRetry={handleRetry} />
          )}

          {results && (
            <AdResults results={results} onReset={reset} />
          )}
        </div>
      </main>
    </div>
  )
}

export default App