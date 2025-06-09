export default function BookCard({ book, onEdit, onDelete }) {
  return (
    <div className="card hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
      <h3 className="text-lg font-semibold text-primary-600 mb-2">
        {book.titulo}
      </h3>
      
      <div className="space-y-1 text-sm text-gray-600 mb-4">
        <p><strong>Autor:</strong> {book.autor}</p>
        {book.ano && <p><strong>Ano:</strong> {book.ano}</p>}
        {book.genero && <p><strong>Gênero:</strong> {book.genero}</p>}
        {book.isbn && <p><strong>ISBN:</strong> {book.isbn}</p>}
        {book.paginas && <p><strong>Páginas:</strong> {book.paginas}</p>}
        {book.descricao && (
          <p className="mt-2">
            <strong>Descrição:</strong> 
            <span className="block mt-1 text-gray-500">
              {book.descricao.length > 100 
                ? book.descricao.substring(0, 100) + '...' 
                : book.descricao
              }
            </span>
          </p>
        )}
      </div>

      <div className="flex justify-between items-center pt-4 border-t border-gray-200">
        <small className="text-gray-400">
          {book.criado_em && new Date(book.criado_em).toLocaleDateString('pt-BR')}
        </small>
        
        <div className="flex gap-2">
          <button
            onClick={() => onEdit(book)}
            className="btn-warning text-xs"
          >
            ✏️ Editar
          </button>
          <button
            onClick={() => onDelete(book.id, book.titulo)}
            className="btn-danger text-xs"
          >
            🗑️ Excluir
          </button>
        </div>
      </div>
    </div>
  );
} 