/**
 * Logger profesional con Winston
 */
import winston from 'winston';
import chalk from 'chalk';

const customFormat = winston.format.printf(({ level, message, timestamp }) => {
  const ts = chalk.gray(timestamp);
  let levelColor;

  switch (level) {
    case 'error':
      levelColor = chalk.red.bold(level.toUpperCase());
      break;
    case 'warn':
      levelColor = chalk.yellow.bold(level.toUpperCase());
      break;
    case 'info':
      levelColor = chalk.blue.bold(level.toUpperCase());
      break;
    case 'debug':
      levelColor = chalk.magenta.bold(level.toUpperCase());
      break;
    default:
      levelColor = level.toUpperCase();
  }

  return `${ts} [${levelColor}] ${message}`;
});

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    customFormat
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'bot-error.log', level: 'error' }),
    new winston.transports.File({ filename: 'bot-combined.log' })
  ]
});

// Funciones helper con colores
export const logSuccess = (message: string) => {
  logger.info(chalk.green('✓ ') + message);
};

export const logError = (message: string, error?: any) => {
  logger.error(chalk.red('✗ ') + message);
  if (error) {
    logger.error(chalk.red(error.message || error));
  }
};

export const logWarning = (message: string) => {
  logger.warn(chalk.yellow('⚠ ') + message);
};

export const logTrade = (message: string) => {
  logger.info(chalk.cyan('💱 ') + message);
};

export const logStats = (message: string) => {
  logger.info(chalk.magenta('📊 ') + message);
};
