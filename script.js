 document.addEventListener('DOMContentLoaded', function () {
            // Variáveis globais
            let currentStep = 1;

            // Elementos da navegação
            const nextStepBtn = document.getElementById('next-step-btn');
            const prevStepBtn = document.getElementById('prev-step-btn');
            const simulateBtn = document.getElementById('simulate-btn');
            const step1Content = document.getElementById('step1-content');
            const step2Content = document.getElementById('step2-content');
            const steps = document.querySelectorAll('.step');

            // Configurar eventos de navegação
            if (nextStepBtn) {
                nextStepBtn.addEventListener('click', function () {
                    if (validateStep1()) {
                        goToStep(2);
                    }
                });
            }

            if (prevStepBtn) {
                prevStepBtn.addEventListener('click', function () {
                    goToStep(1);
                });
            }

            if (simulateBtn) {
                simulateBtn.addEventListener('click', function () {
                    if (validateStep2()) {
                        calculateSimulation();
                        // Ir para a página de resultados
                        document.getElementById('questionnaire').classList.remove('active');
                        document.getElementById('results').classList.add('active');
                        window.scrollTo(0, 0);
                    }
                });
            }

            // Função para navegar entre as etapas
            function goToStep(step) {
                // Esconder todos os conteúdos de etapa
                step1Content.style.display = 'none';
                step2Content.style.display = 'none';

                // Remover classe ativa de todos os indicadores
                steps.forEach(s => s.classList.remove('active'));

                // Mostrar conteúdo da etapa atual e atualizar indicador
                if (step === 1) {
                    step1Content.style.display = 'block';
                    document.querySelector('.step[data-step="1"]').classList.add('active');
                    currentStep = 1;
                } else if (step === 2) {
                    step2Content.style.display = 'block';
                    document.querySelector('.step[data-step="2"]').classList.add('active');
                    currentStep = 2;
                }
            }

            // Validação da Etapa 1
            function validateStep1() {
                const paymentMethod = document.getElementById('payment-method').value;

                if (!paymentMethod) {
                    alert('Por favor, selecione a forma de pagamento.');
                    return false;
                }

                // Validações adicionais para financiamento
                if (paymentMethod === 'financing') {
                    const giveDownpayment = document.getElementById('give-downpayment').value;

                    if (giveDownpayment === 'yes') {
                        const downpaymentValue = document.getElementById('downpayment-value').value;
                        if (!downpaymentValue || isNaN(downpaymentValue) || parseFloat(downpaymentValue) <= 0) {
                            alert('Por favor, informe um valor válido para a entrada.');
                            return false;
                        }
                    }

                    const monthlyPayment = document.getElementById('monthly-payment').value;
                    if (!monthlyPayment || isNaN(monthlyPayment) || parseFloat(monthlyPayment) <= 0) {
                        alert('Por favor, informe um valor válido para a parcela mensal.');
                        return false;
                    }
                }

                // Validações para quem possui carro
                const hasCar = document.getElementById('has-car').value;
                if (hasCar === 'yes') {
                    const carPaid = document.getElementById('car-paid').value;
                    if (carPaid === 'no') {
                        const remainingDebt = document.getElementById('remaining-debt').value;
                        if (!remainingDebt || isNaN(remainingDebt) || parseFloat(remainingDebt) <= 0) {
                            alert('Por favor, informe um valor válido para o valor que falta quitar.');
                            return false;
                        }
                    }
                }

                return true;
            }

            // Validação da Etapa 2
            function validateStep2() {
                const carType = document.getElementById('car-type').value;
                const carCondition = document.getElementById('car-condition').value;
                const carCategory = document.getElementById('car-category').value;
                const carBrand = document.getElementById('car-brand').value;
                const primaryUse = document.getElementById('primary-use').value;
                const purchaseTime = document.getElementById('purchase-time').value;

                if (!carType || !carCondition || !carCategory || !carBrand || !primaryUse || !purchaseTime) {
                    alert('Por favor, preencha todos os campos obrigatórios.');
                    return false;
                }

                // Validação adicional para carro usado
                if (carCondition === 'used') {
                    const minYear = document.getElementById('min-year').value;
                    if (!minYear || isNaN(minYear) || parseInt(minYear) < 1990 || parseInt(minYear) > new Date().getFullYear()) {
                        alert('Por favor, informe um ano válido para o carro usado.');
                        return false;
                    }
                }

                return true;
            }

            // Configurar interações dinâmicas na Etapa 1
            const paymentMethod = document.getElementById('payment-method');
            const hasCar = document.getElementById('has-car');
            const carPaid = document.getElementById('car-paid');

            if (paymentMethod) {
                paymentMethod.addEventListener('change', function () {
                    const financingFields = document.getElementById('financing-fields');
                    if (this.value === 'financing') {
                        financingFields.style.display = 'block';
                    } else {
                        financingFields.style.display = 'none';
                    }
                });
            }

            if (hasCar) {
                hasCar.addEventListener('change', function () {
                    const carPaidGroup = document.getElementById('car-paid-group');
                    if (this.value === 'yes') {
                        carPaidGroup.style.display = 'block';
                    } else {
                        carPaidGroup.style.display = 'none';
                        document.getElementById('remaining-debt-group').style.display = 'none';
                    }
                });
            }

            if (carPaid) {
                carPaid.addEventListener('change', function () {
                    const remainingDebtGroup = document.getElementById('remaining-debt-group');
                    if (this.value === 'no') {
                        remainingDebtGroup.style.display = 'block';
                    } else {
                        remainingDebtGroup.style.display = 'none';
                    }
                });
            }

            // Configurar interações dinâmicas na Etapa 2
            const carCondition = document.getElementById('car-condition');
            if (carCondition) {
                carCondition.addEventListener('change', function () {
                    const minYearGroup = document.getElementById('min-year-group');
                    if (this.value === 'used') {
                        minYearGroup.style.display = 'block';
                    } else {
                        minYearGroup.style.display = 'none';
                    }
                });
            }

            // Configurar campo de entrada para financiamento
            const giveDownpayment = document.getElementById('give-downpayment');
            if (giveDownpayment) {
                giveDownpayment.addEventListener('change', function () {
                    const downpaymentField = document.getElementById('downpayment-field');
                    if (this.value === 'yes') {
                        downpaymentField.style.display = 'block';
                    } else {
                        downpaymentField.style.display = 'none';
                    }
                });
            }

            // Navegação entre páginas principais
            const navLinks = document.querySelectorAll('.nav-links a, .cta-button');
            const pages = document.querySelectorAll('.page');

            navLinks.forEach(link => {
                link.addEventListener('click', function (e) {
                    e.preventDefault();
                    const targetPage = this.getAttribute('data-page');

                    if (targetPage) {
                        pages.forEach(page => {
                            page.classList.remove('active');
                        });

                        document.getElementById(targetPage).classList.add('active');
                        window.scrollTo(0, 0);

                        // Se for para o questionário, resetar para a primeira etapa
                        if (targetPage === 'questionnaire') {
                            goToStep(1);
                        }
                    }
                });
            });

            // Função de simulação (exemplo)
            function calculateSimulation() {
                // Aqui viria a lógica de cálculo da simulação
                console.log('Simulação calculada!');

                // Exemplo de preenchimento dos resultados
                document.getElementById('cash-total').textContent = 'R$ 75.000,00';
                document.getElementById('cash-discount').textContent = 'R$ 3.750,00';
                document.getElementById('cash-final').textContent = 'R$ 71.250,00';
                document.getElementById('result-car-model').textContent = 'Volkswagen Golf 2023';
                document.getElementById('result-car-price').textContent = 'R$ 75.000,00';
                document.getElementById('result-car-options').textContent = 'Automático, Ar-condicionado, Multimídia';

                document.getElementById('financing-total').textContent = 'R$ 75.000,00';
                document.getElementById('financing-downpayment').textContent = 'R$ 15.000,00';
                document.getElementById('financing-amount').textContent = 'R$ 60.000,00';
                document.getElementById('financing-installments').textContent = '48x';
                document.getElementById('financing-monthly').textContent = 'R$ 1.450,00';
                document.getElementById('financing-totalpaid').textContent = 'R$ 84.600,00';
                document.getElementById('financing-interest').textContent = 'R$ 9.600,00';
                document.getElementById('financing-percentage').textContent = '80% financiado, 20% entrada';
                document.getElementById('financing-car-model').textContent = 'Volkswagen Golf 2023';
                document.getElementById('financing-car-price').textContent = 'R$ 75.000,00';
                document.getElementById('financing-car-options').textContent = 'Automático, Ar-condicionado, Multimídia';
                document.getElementById('monthly-savings').textContent = 'R$ 250,00';
                document.getElementById('ideal-purchase-time').textContent = '3 meses';

                // Mostrar o resultado correto baseado no tipo de pagamento
                const paymentMethod = document.getElementById('payment-method').value;
                if (paymentMethod === 'cash') {
                    document.getElementById('cash-result').style.display = 'block';
                    document.getElementById('financing-result').style.display = 'none';
                } else {
                    document.getElementById('cash-result').style.display = 'none';
                    document.getElementById('financing-result').style.display = 'block';

                    // Criar gráficos
                    createCharts();
                }
            }

            // Criar gráficos para financiamento
            function createCharts() {
                // Gráfico de composição do financiamento
                const financingCtx = document.getElementById('financingChart');
                if (financingCtx) {
                    new Chart(financingCtx, {
                        type: 'pie',
                        data: {
                            labels: ['Valor do Veículo', 'Juros'],
                            datasets: [{
                                data: [75000, 9600],
                                backgroundColor: ['#ff2800', '#d9d9d9'],
                                borderWidth: 0
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'bottom',
                                    labels: {
                                        color: '#d9d9d9',
                                        font: { size: 12 }
                                    }
                                }
                            }
                        }
                    });
                }

                // Gráfico de comparação de parcelas
                const comparisonCtx = document.getElementById('comparisonChart');
                if (comparisonCtx) {
                    new Chart(comparisonCtx, {
                        type: 'bar',
                        data: {
                            labels: ['Parcela Atual', 'Nova Parcela'],
                            datasets: [{
                                label: 'Valor da Parcela (R$)',
                                data: [1700, 1450],
                                backgroundColor: ['#d9d9d9', '#ff2800'],
                                borderWidth: 0
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    ticks: { color: '#d9d9d9' },
                                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                                },
                                x: {
                                    ticks: { color: '#d9d9d9' },
                                    grid: { display: false }
                                }
                            },
                            plugins: {
                                legend: { display: false }
                            }
                        }
                    });
                }
            }
        });
   