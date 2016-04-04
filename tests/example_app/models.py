# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatedFields, TranslatableModel

from knocker.mixins import KnockerModel
from knocker.signals import notify_items
from meta.models import ModelMeta


class Post(KnockerModel, ModelMeta, models.Model):
    """
    Blog post
    """
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('slug'))
    abstract = models.TextField(_('Abstract'))
    meta_description = models.TextField(
        verbose_name=_(u'Post meta description'),
        blank=True, default='')
    meta_keywords = models.TextField(verbose_name=_(u'Post meta keywords'),
                                     blank=True, default='')
    author = models.ForeignKey(User, verbose_name=_('Author'), null=True,
                               blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(_('Published Since'),
                                          default=timezone.now)
    date_published_end = models.DateTimeField(_('Published Until'), null=True,
                                              blank=True)
    main_image = models.ImageField(verbose_name=_('Main image'), blank=True,
                                   upload_to='images', null=True)
    text = models.TextField(verbose_name=_(u'Post text'),
                            blank=True, default='')
    image_url = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('blog article')
        verbose_name_plural = _('blog articles')
        ordering = ("-date_published", "-date_created")
        get_latest_by = 'date_published'

    def get_title(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})


class MultiLanguagePost(KnockerModel, ModelMeta, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=255),
        slug=models.SlugField(_('slug'), blank=True, db_index=True),
    )

    class Meta:
        verbose_name = _('multilanguage blog article')
        verbose_name_plural = _('multilanguage blog articles')

    def get_title(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('parler-post-detail', kwargs={'slug': self.slug})

    def should_knock(self, created=False):
        return self.get_current_language() != 'fr'


class NoKnockPost(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), blank=True, db_index=True)

    class Meta:
        verbose_name = _('no knocj blog article')
        verbose_name_plural = _('no knocj blog articles')


post_save.connect(notify_items, sender=NoKnockPost)