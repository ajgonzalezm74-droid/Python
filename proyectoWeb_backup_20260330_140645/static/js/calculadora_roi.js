// ========= MODAL CALCULADORA =========
  const modal = document.getElementById('modalCalculadora');
  const openCalcBtn = document.getElementById('openCalcBtnHeader');
  const closeModalBtn = document.getElementById('closeModalBtn');
  
  openCalcBtn.addEventListener('click', (e) => {
    e.preventDefault();
    modal.style.display = 'flex';
  });
  closeModalBtn.addEventListener('click', () => { modal.style.display = 'none'; });
  window.addEventListener('click', (e) => { if (e.target === modal) modal.style.display = 'none'; });
  
  function computeROI() {
    let inv = parseFloat(document.getElementById('investment').value) || 0;
    let monthly = parseFloat(document.getElementById('monthlySaving').value) || 0;
    let months = parseInt(document.getElementById('months').value) || 1;
    if (inv <= 0) { document.getElementById('resultDisplay').innerHTML = "⚠️ Ingresa inversión válida"; return; }
    const totalBenefit = monthly * months;
    const roi = ((totalBenefit - inv) / inv) * 100;
    document.getElementById('resultDisplay').innerHTML = `🚀 ROI: ${roi.toFixed(1)}% &nbsp; | &nbsp; Beneficio neto: $${(totalBenefit - inv).toFixed(2)} USD`;
  }
  document.getElementById('calculateBtn').addEventListener('click', computeROI);
  computeROI();
  
  