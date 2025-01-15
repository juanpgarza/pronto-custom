==================================
pronto_account_cashbox
==================================

Adaptaciones solicitadas por Pronto:

#. Confirmación de arqueo inicial
#. Vista de lista de los pagos agrupados por caja, sesión y diario
#. Sesión por defecto en el ingreso de los pagos
#. Reporte de movimientos de caja
#. Archivo de datos de configuración de cajas: FSM, PIN, DR
#. Control saldo inicial informado con saldo última sesión
#. Integración con gastos de empleados (hr.expense)
#. Integración con Cobros y Pagos
#. Motivos de Recibos y Pagos desde caja
#. Transferencias de efectivo entre cajas
[to-do] La transferencia de efectivo entre caja genera asientos contables para los payments origen y destino.
Estos payments tienen asociados asientos contables. Se necesita poder marcar las transferencias para que los asientos generados
los marque como "En clima". Por ahora se lo resolví con una AS a nivel de sesion de caja.
