import { useState } from 'react'
import { apiClient, ApiError } from './api'
import { AdCopyGenerationRequest, GeneratedAdCopy } from '@/types/api'

export function useAdGeneration() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [results, setResults] = useState<GeneratedAdCopy[] | null>(null)

  const generateAdCopy = async (request: AdCopyGenerationRequest) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await apiClient.generateAdCopy(request)
      setResults(response.generatedCopies)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('予期しないエラーが発生しました')
      }
      setResults(null)
    } finally {
      setIsLoading(false)
    }
  }

  const reset = () => {
    setError(null)
    setResults(null)
    setIsLoading(false)
  }

  return {
    isLoading,
    error,
    results,
    generateAdCopy,
    reset
  }
}