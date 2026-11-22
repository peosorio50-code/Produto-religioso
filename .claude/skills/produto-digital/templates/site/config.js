/* ============================================================
   O Santo do Nosso Casamento — CONFIGURAÇÃO DO SITE
   É o único arquivo que você precisa editar antes de subir.
   ============================================================ */
window.CFG = {
  API: "https://api.mapadaalma.online",         // o servidor (o mesmo do Meu Santo Protetor)
  CHECKOUT: "",                                  // link do checkout na Kiwify (reserva: só é usado se o servidor não responder). Ex.: "https://pay.kiwify.com.br/AbCdEf1"
  PRECO: "37",                                   // preço mostrado na oferta (o preço que vale é o da Kiwify: mantenha igual)
  PIXEL: "1108457205151516",                     // pixel do Meta (o mesmo do Meu Santo Protetor)
  CONTATO: "contato@meusantoprotetor.online",    // e-mail de atendimento mostrado no rodapé
  SITE_SANTO: "https://meusantoprotetor.online", // site principal (link do rodapé)
  VENDA_ABERTA: true,                            // false = esconde o botão de comprar (o quiz grátis continua)

  // Página de obrigado (upsell de 1 clique da Kiwify). Vazio = a página pula a oferta e mostra o livro.
  UPSELL_ID: "",                                 // o trecho depois de "kiwify-upsell-trigger-" no código que a Kiwify gera
  UPSELL_SCRIPT: "https://snippets.kiwify.com/upsell/upsell.min.js", // confira com o <script> do código que a Kiwify gera; se for outro, troque aqui
  CHECKOUT_UPSELL: "",                           // link do checkout da mesma oferta (reserva para quem pagou no Pix, que não tem 1 clique)
  PRECO_UPSELL: "27",                            // preço da oferta na página de obrigado
  PRECO_CHEIO_UPSELL: "47"                       // preço normal do produto do upsell (Os Santos Protetores da Sua Família)
};
