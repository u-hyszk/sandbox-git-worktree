import { render, screen, fireEvent } from '@testing-library/react'
import { AdGenerationForm } from '@/components/specific/ad-generation-form'

describe('AdGenerationForm', () => {
  const mockOnSubmit = jest.fn()

  beforeEach(() => {
    mockOnSubmit.mockClear()
  })

  it('renders form fields correctly', () => {
    render(<AdGenerationForm onSubmit={mockOnSubmit} isLoading={false} />)
    
    expect(screen.getByLabelText('商品・サービス名')).toBeInTheDocument()
    expect(screen.getByLabelText('ターゲット層')).toBeInTheDocument()
    expect(screen.getByLabelText('アピールポイント')).toBeInTheDocument()
    expect(screen.getByText('広告文を生成')).toBeInTheDocument()
  })

  it('disables submit button when form is invalid', () => {
    render(<AdGenerationForm onSubmit={mockOnSubmit} isLoading={false} />)
    
    const submitButton = screen.getByText('広告文を生成')
    expect(submitButton).toBeDisabled()
  })

  it('enables submit button when form is valid', () => {
    render(<AdGenerationForm onSubmit={mockOnSubmit} isLoading={false} />)
    
    fireEvent.change(screen.getByLabelText('商品・サービス名'), {
      target: { value: 'テスト商品' }
    })
    fireEvent.change(screen.getByLabelText('ターゲット層'), {
      target: { value: 'テストターゲット' }
    })
    
    fireEvent.change(screen.getByLabelText('アピールポイント'), {
      target: { value: 'テストポイント' }
    })
    fireEvent.click(screen.getByText('追加'))
    
    const submitButton = screen.getByText('広告文を生成')
    expect(submitButton).not.toBeDisabled()
  })
})