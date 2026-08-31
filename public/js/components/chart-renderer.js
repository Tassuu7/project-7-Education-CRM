'use strict';

/**
 * Interactive HTML5 Canvas Charts Engine (Funnel & Bar Visualizations)
 */

class ChartRenderer {
  static drawFunnel(canvasId, funnelData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 400;
    const height = canvas.height = 240;

    ctx.clearRect(0, 0, width, height);

    const stages = Object.entries(funnelData);
    if (stages.length === 0) return;

    const maxVal = Math.max(...stages.map(s => s[1]), 1);
    const barHeight = 24;
    const gap = 12;
    const colors = ['#6366f1', '#818cf8', '#a5b4fc', '#06b6d4', '#10b981', '#f59e0b'];

    stages.forEach(([stage, count], index) => {
      const y = index * (barHeight + gap) + 15;
      const barWidth = Math.max(20, (count / maxVal) * (width - 150));

      // Label
      ctx.fillStyle = '#64748b';
      ctx.font = '12px Inter, sans-serif';
      ctx.fillText(stage.replace('_', ' ').toUpperCase(), 10, y + 16);

      // Bar
      ctx.fillStyle = colors[index % colors.length];
      ctx.beginPath();
      ctx.roundRect(140, y, barWidth, barHeight, [4]);
      ctx.fill();

      // Count
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.fillText(count.toString(), 148, y + 16);
    });
  }
}

window.ChartRenderer = ChartRenderer;
