/**
 * Punto de entrada principal del bot de copy trading
 */
import { CopyTradingBot } from './services/CopyTradingBot';
import { loadConfig } from './utils/config';
import { logger, logError, logSuccess } from './utils/logger';
import chalk from 'chalk';

async function main() {
  let bot: CopyTradingBot | null = null;

  try {
    // Cargar configuración
    const config = loadConfig();

    // Crear e inicializar el bot
    bot = new CopyTradingBot(config);
    await bot.initialize();

    // Manejar señales de terminación
    const gracefulShutdown = () => {
      logger.info('');
      logger.info(chalk.yellow('Señal de terminación recibida...'));
      if (bot) {
        bot.stop();
      }
      process.exit(0);
    };

    process.on('SIGINT', gracefulShutdown);
    process.on('SIGTERM', gracefulShutdown);

    // Iniciar el bot
    await bot.start();

  } catch (error: any) {
    logError('Error fatal en el bot', error);
    process.exit(1);
  }
}

// Ejecutar
main().catch((error) => {
  logError('Error no capturado', error);
  process.exit(1);
});
