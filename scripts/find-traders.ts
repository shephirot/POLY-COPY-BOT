/**
 * Script auxiliar para encontrar y analizar traders en Polymarket
 * Uso: ts-node scripts/find-traders.ts <trader_address>
 */
import axios from 'axios';
import chalk from 'chalk';

interface TraderStats {
  totalTrades: number;
  totalVolume: number;
  winRate: number;
  avgOrderSize: number;
  mostTradedMarkets: Map<string, number>;
}

async function getTraderTrades(address: string, limit: number = 100) {
  try {
    const url = 'https://clob.polymarket.com/data/trades';
    const response = await axios.get(url, {
      params: {
        maker_address: address.toLowerCase(),
        limit: limit
      }
    });
    return response.data;
  } catch (error: any) {
    console.error(chalk.red('Error al obtener trades:'), error.message);
    return [];
  }
}

async function analyzeTrader(address: string): Promise<void> {
  console.log(chalk.bold.cyan('\n🔍 Analizando trader...\n'));
  console.log(`Dirección: ${chalk.yellow(address)}\n`);

  const trades = await getTraderTrades(address, 200);

  if (!trades || trades.length === 0) {
    console.log(chalk.red('❌ No se encontraron trades para este trader'));
    console.log(chalk.yellow('\nPosibles razones:'));
    console.log('  - La dirección es incorrecta');
    console.log('  - El trader no ha realizado operaciones recientemente');
    console.log('  - Problemas de conexión con la API\n');
    return;
  }

  // Calcular estadísticas
  const stats: TraderStats = {
    totalTrades: trades.length,
    totalVolume: 0,
    winRate: 0,
    avgOrderSize: 0,
    mostTradedMarkets: new Map()
  };

  let totalSize = 0;

  for (const trade of trades) {
    const size = parseFloat(trade.size);
    const price = parseFloat(trade.price);
    const volume = size * price;

    stats.totalVolume += volume;
    totalSize += size;

    // Contar mercados
    const count = stats.mostTradedMarkets.get(trade.market) || 0;
    stats.mostTradedMarkets.set(trade.market, count + 1);
  }

  stats.avgOrderSize = stats.totalVolume / stats.totalTrades;

  // Obtener top 5 mercados
  const topMarkets = Array.from(stats.mostTradedMarkets.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  // Imprimir resultados
  console.log(chalk.bold('📊 ESTADÍSTICAS DEL TRADER\n'));
  console.log('═'.repeat(60));
  console.log(`${chalk.bold('Total de trades:')} ${chalk.green(stats.totalTrades)}`);
  console.log(
    `${chalk.bold('Volumen total:')} ${chalk.green('$' + stats.totalVolume.toFixed(2))}`
  );
  console.log(
    `${chalk.bold('Tamaño promedio de orden:')} ${chalk.green('$' + stats.avgOrderSize.toFixed(2))}`
  );
  console.log('═'.repeat(60));

  console.log(chalk.bold('\n🎯 Top 5 Mercados Más Operados:\n'));
  topMarkets.forEach(([market, count], index) => {
    console.log(`${index + 1}. ${chalk.cyan(market.substring(0, 20) + '...')} - ${chalk.yellow(count)} trades`);
  });

  // Trades recientes
  console.log(chalk.bold('\n📈 Últimos 5 Trades:\n'));
  const recentTrades = trades.slice(0, 5);
  recentTrades.forEach((trade: any, index: number) => {
    const date = new Date(trade.timestamp).toLocaleString();
    const side = trade.side === 'BUY' ? chalk.green('BUY ') : chalk.red('SELL');
    const size = parseFloat(trade.size).toFixed(2);
    const price = parseFloat(trade.price).toFixed(3);

    console.log(`${index + 1}. ${side} ${chalk.yellow(size)} @ $${chalk.cyan(price)} - ${chalk.gray(date)}`);
  });

  console.log(chalk.bold.green('\n✅ Análisis completado\n'));

  // Recomendaciones
  console.log(chalk.bold.yellow('💡 RECOMENDACIONES:\n'));

  if (stats.avgOrderSize < 10) {
    console.log(
      chalk.yellow('  ⚠ Este trader opera con órdenes pequeñas (< $10 promedio)')
    );
    console.log(chalk.yellow('    Considera usar COPY_SIZE_MULTIPLIER mayor a 1.0\n'));
  } else if (stats.avgOrderSize > 500) {
    console.log(
      chalk.yellow('  ⚠ Este trader opera con órdenes grandes (> $500 promedio)')
    );
    console.log(chalk.yellow('    Considera usar COPY_SIZE_MULTIPLIER menor a 1.0\n'));
  } else {
    console.log(chalk.green('  ✓ Tamaño de orden promedio razonable\n'));
  }

  if (stats.totalTrades < 10) {
    console.log(chalk.yellow('  ⚠ Pocos trades históricos - trader poco activo\n'));
  } else if (stats.totalTrades > 100) {
    console.log(chalk.green('  ✓ Trader muy activo con buen historial\n'));
  }

  console.log(chalk.bold('📝 Configuración sugerida para .env:\n'));
  console.log(chalk.gray('  TARGET_TRADER_ADDRESS=' + address));

  if (stats.avgOrderSize > 100) {
    console.log(chalk.gray('  COPY_SIZE_MULTIPLIER=0.5'));
    console.log(chalk.gray('  MAX_ORDER_SIZE=100'));
  } else {
    console.log(chalk.gray('  COPY_SIZE_MULTIPLIER=1.0'));
    console.log(chalk.gray('  MAX_ORDER_SIZE=50'));
  }

  console.log();
}

// Main
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log(chalk.red('\n❌ Error: Debes proporcionar una dirección de trader\n'));
  console.log(chalk.yellow('Uso: ts-node scripts/find-traders.ts <trader_address>\n'));
  console.log(chalk.gray('Ejemplo:'));
  console.log(chalk.gray('  ts-node scripts/find-traders.ts 0x1234567890abcdef...\n'));
  process.exit(1);
}

const traderAddress = args[0];

if (!traderAddress.startsWith('0x') || traderAddress.length !== 42) {
  console.log(chalk.red('\n❌ Error: La dirección no parece válida\n'));
  console.log(chalk.yellow('La dirección debe:'));
  console.log(chalk.yellow('  - Empezar con 0x'));
  console.log(chalk.yellow('  - Tener 42 caracteres de longitud\n'));
  process.exit(1);
}

analyzeTrader(traderAddress).catch(error => {
  console.error(chalk.red('\n❌ Error inesperado:'), error.message);
  process.exit(1);
});
