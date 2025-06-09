import { useState, useEffect } from 'react';
import { booksService } from '../services/api';
import BookCard from './BookCard';
import BookForm from './BookForm';

export default function Dashboard({ user, onLogout }) {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [pagination, setPagination] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingBook, setEditingBook] = useState(null);

  useEffect(() => {
    loadBooks();
  }, [currentPage]);

  const loadBooks = async () => {
    setLoading(true);
    try {
      const data = await booksService.getBooks(currentPage);
      setBooks(data.livros || []);
      setPagination(data.paginacao);
    } catch (error) {
      alert('Erro ao carregar livros: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      loadBooks();
      return;
    }
    
    setLoading(true);
    try {
      const data = await booksService.searchBooks(searchTerm);
      setBooks(data.livros || []);
      setPagination(null);
    } catch (error) {
      alert('Erro na busca: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddBook = async (bookData) => {
    try {
      await booksService.createBook(bookData);
      setShowAddForm(false);
      loadBooks();
      alert('Livro adicionado com sucesso!');
    } catch (error) {
      alert('Erro ao adicionar livro: ' + error.response?.data?.detalhes || error.message);
    }
  };

  const handleEditBook = async (bookData) => {
    try {
      await booksService.updateBook(editingBook.id, bookData);
      setEditingBook(null);
      loadBooks();
      alert('Livro atualizado com sucesso!');
    } catch (error) {
      alert('Erro ao atualizar livro: ' + error.response?.data?.detalhes || error.message);
    }
  };

  const handleDeleteBook = async (id, titulo) => {
    if (!window.confirm(`Tem certeza que deseja excluir "${titulo}"?`)) return;
    
    try {
      await booksService.deleteBook(id);
      loadBooks();
      alert('Livro excluído com sucesso!');
    } catch (error) {
      alert('Erro ao excluir livro: ' + error.response?.data?.detalhes || error.message);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white/10 backdrop-blur-md p-4 mb-6">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-white">📚 Biblioteca</h1>
          <div className="flex items-center gap-4">
            <span className="text-white">Olá, {user.nome || user.email}</span>
            <button onClick={onLogout} className="btn-secondary">
              Sair
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto p-4">
        {/* Barra de busca e ações */}
        <div className="card mb-6">
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
            <div className="flex gap-2 flex-1">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Buscar livros..."
                className="input-field"
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              />
              <button onClick={handleSearch} className="btn-secondary">
                🔍 Buscar
              </button>
              <button onClick={loadBooks} className="btn-secondary">
                📋 Todos
              </button>
            </div>
            <button
              onClick={() => setShowAddForm(true)}
              className="btn-primary"
            >
              ➕ Adicionar Livro
            </button>
          </div>
        </div>

        {/* Lista de livros */}
        {loading ? (
          <div className="text-center py-8">
            <div className="text-white text-lg">Carregando...</div>
          </div>
        ) : books.length === 0 ? (
          <div className="card text-center py-8">
            <p className="text-gray-600">Nenhum livro encontrado.</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {books.map((book) => (
                <BookCard
                  key={book.id}
                  book={book}
                  onEdit={setEditingBook}
                  onDelete={handleDeleteBook}
                />
              ))}
            </div>

            
          </>
        )}
      </div>

      {/* Modais */}
      {showAddForm && (
        <BookForm
          onSubmit={handleAddBook}
          onCancel={() => setShowAddForm(false)}
          title="Adicionar Novo Livro"
        />
      )}

      {editingBook && (
        <BookForm
          book={editingBook}
          onSubmit={handleEditBook}
          onCancel={() => setEditingBook(null)}
          title="Editar Livro"
        />
      )}
    </div>
  );
} 