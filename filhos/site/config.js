/* ============================================================
   Novena pelos Filhos — CONFIGURAÇÃO DO SITE
   É o único arquivo que você precisa editar antes de subir.
   ============================================================ */
window.CFG = {
  API: "https://api.mapadaalma.online",         // o servidor (o mesmo do Meu Santo Protetor)
  CHECKOUT: "",                                  // link do checkout na Kiwify (reserva: só é usado se o servidor não responder). Ex.: "https://pay.kiwify.com.br/AbCdEf1"
  PRECO: "87",                                   // preço mostrado na oferta (o preço que vale é o da Kiwify: mantenha igual)
  PIXEL: "1108457205151516",                     // pixel do Meta (o mesmo do Meu Santo Protetor)
  CONTATO: "contato@meusantoprotetor.online",    // e-mail de atendimento mostrado no rodapé
  SITE_SANTO: "https://meusantoprotetor.online", // site principal (link do rodapé)
  VENDA_ABERTA: true,                            // false = esconde o botão de comprar (o quiz grátis continua)

  // VSL da página de vendas (o vídeo do Carlos). Vazio = a página fica sem vídeo.
  VSL_SRC: "",                                   // ex.: "videos/vsl.mp4" (até 25 MB no Cloudflare Pages)
  VSL_POSTER: "img/vsl-capa.jpg",                // imagem que aparece antes de o vídeo carregar
  VSL_TOPO: false,                               // true = a VSL aparece no topo, antes do quiz; false = depois da revelação (padrão)

  // Os vídeos da novena (página novena.html). Pode ser um arquivo do site ("videos/dia1.mp4")
  // ou um vídeo não listado do YouTube ("youtube:ID_DO_VIDEO"). Vazio = a página mostra só o texto do dia.
  VIDEOS: {
    dia1: "", dia2: "", dia3: "", dia4: "", dia5: "", dia6: "", dia7: "", dia8: "", dia9: "",
    terco: ""                                    // o vídeo do terço (order bump)
  },

  // Página de obrigado (upsell de 1 clique da Kiwify: Um Livro para Cada Filho). Vazio = a página pula a oferta e mostra a novena.
  UPSELL_ID: "",                                 // o trecho depois de "kiwify-upsell-trigger-" no código que a Kiwify gera
  UPSELL_SCRIPT: "https://snippets.kiwify.com/upsell/upsell.min.js", // confira com o <script> do código que a Kiwify gera; se for outro, troque aqui
  CHECKOUT_UPSELL: "",                           // link do checkout da mesma oferta (reserva para quem pagou no Pix, que não tem 1 clique)
  PRECO_UPSELL: "37"                             // preço do upsell (só existe nesta página)
};
