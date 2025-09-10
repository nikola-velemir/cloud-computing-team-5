import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'timeFormat',
  standalone: false,
})
export class TimeFormatPipe implements PipeTransform {
  transform(value: number, ...args: unknown[]): string {
    if (typeof value !== 'number' || isNaN(value)) return 'Invalid value';

    const hours = Math.floor(value / 3600);
    const minutes = Math.floor(value / 60);
    const seconds = Math.floor(value % 60);
    let output = '';
    if (hours > 0) output += hours + ':';
    if (minutes > 0)
      if (minutes > 10) output += minutes + ':';
      else output += '0' + minutes + ':';
    if (seconds > 10) output += seconds;
    else output += '0' + seconds;
    return output;
  }
}
